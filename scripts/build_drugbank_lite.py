"""Build an approximately target-sized DrugBank lite XML from the full XML.

Usage:
    python scripts/build_drugbank_lite.py \
        --input "static/full database.xml" \
        --output "static/drugbank_lite.xml" \
        --target-mb 80
"""

from __future__ import annotations

import argparse
import os
import xml.etree.ElementTree as ET


def _split_tag(tag: str) -> tuple[str | None, str]:
    if tag.startswith("{") and "}" in tag:
        uri, local = tag[1:].split("}", 1)
        return uri, local
    return None, tag


def build_lite_xml(input_path: str, output_path: str, target_mb: int) -> tuple[int, int]:
    target_bytes = target_mb * 1024 * 1024
    minimum_fill_bytes = int(target_bytes * 0.98)

    context = ET.iterparse(input_path, events=("start", "end"))
    root = None
    namespace_uri = None
    depth = 0

    with open(output_path, "wb") as out:
        out.write(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")

        kept = 0
        reached_target = False

        for event, elem in context:
            if event == "start" and root is None:
                root = elem
                namespace_uri, root_local = _split_tag(root.tag)
                if namespace_uri:
                    ET.register_namespace("", namespace_uri)
                    out.write(f"<{root_local} xmlns=\"{namespace_uri}\">\n".encode("utf-8"))
                else:
                    out.write(f"<{root_local}>\n".encode("utf-8"))
                depth = 1
                continue

            if event == "start":
                depth += 1
                continue

            if event != "end":
                continue

            _, local = _split_tag(elem.tag)
            is_top_level_drug = local == "drug" and depth == 2
            if not is_top_level_drug:
                depth -= 1
                continue

            elem_bytes = ET.tostring(elem, encoding="utf-8")
            projected_size = out.tell() + len(elem_bytes) + 1
            if kept > 0 and projected_size > target_bytes:
                elem.clear()
                depth -= 1
                if out.tell() >= minimum_fill_bytes:
                    reached_target = True
                    break
                continue

            out.write(elem_bytes)
            out.write(b"\n")
            kept += 1

            if out.tell() >= target_bytes:
                reached_target = True
                depth -= 1
                break

            elem.clear()
            depth -= 1

        if root is None:
            raise RuntimeError("Input XML does not appear to contain a root element")

        _, root_local = _split_tag(root.tag)
        out.write(f"</{root_local}>\n".encode("utf-8"))

    if not reached_target:
        actual_size = os.path.getsize(output_path)
        return kept, actual_size

    return kept, os.path.getsize(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build DrugBank lite XML subset")
    parser.add_argument("--input", required=True, help="Path to full DrugBank XML")
    parser.add_argument("--output", required=True, help="Output path for lite XML")
    parser.add_argument("--target-mb", type=int, default=80, help="Approximate target size in MB")
    args = parser.parse_args()

    kept, size_bytes = build_lite_xml(args.input, args.output, args.target_mb)
    size_mb = size_bytes / (1024 * 1024)

    print(f"Created: {args.output}")
    print(f"Drugs kept: {kept}")
    print(f"File size: {size_bytes} bytes ({size_mb:.2f} MB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
