from xml.etree import ElementTree
import os
from pathlib import Path
import threading
import time
import sys


class DrugBankService:
    """Service class to interact with DrugBank XML database (Singleton Pattern)"""
    
    # Class-level shared cache (singleton pattern)
    _shared_root = None
    _shared_drugs_cache = None
    _loading_lock = threading.Lock()
    _is_loaded = False
    
    def __init__(self):
        self.namespace = {'db': 'http://www.drugbank.ca'}
    
    def _find_drugbank_xml(self):
        """Find DrugBank XML file in common locations"""
        possible_paths = [
            # Static folder (where user placed it)
            Path(__file__).parent.parent / 'static' / 'full database.xml',
            Path(__file__).parent.parent / 'static' / 'drugbank.xml',
            # User's home directory (drugbank_downloader cache)
            Path.home() / '.data' / 'drugbank' / 'full database.xml',
            Path.home() / '.data' / 'drugbank' / 'drugbank.xml',
            # Project data directory
            Path(__file__).parent.parent / 'data' / 'full database.xml',
            Path(__file__).parent.parent / 'data' / 'drugbank.xml',
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    @property
    def root(self):
        """Lazy load DrugBank XML root (Singleton - loads only once)"""
        # Return cached root if already loaded
        if DrugBankService._is_loaded and DrugBankService._shared_root is not None:
            return DrugBankService._shared_root
        
        # Use lock to prevent multiple threads loading simultaneously
        with DrugBankService._loading_lock:
            # Double-check after acquiring lock
            if DrugBankService._is_loaded and DrugBankService._shared_root is not None:
                return DrugBankService._shared_root
            
            xml_path = self._find_drugbank_xml()
            
            if xml_path is None:
                raise FileNotFoundError(
                    "DrugBank XML file not found. Please download it from "
                    "https://go.drugbank.com/releases/latest and place it in:\n"
                    f"{Path(__file__).parent.parent / 'static' / 'full database.xml'}"
                )
            
            print(f"\n{'='*70}")
            print(f"📂 Loading DrugBank database from: {xml_path}")
            print(f"{'='*70}")
            print("⏳ Parsing XML file...", end='', flush=True)
            
            # Progress tracking with timer
            start_time = time.time()
            stop_progress = threading.Event()
            
            def show_progress():
                dot_count = 0
                while not stop_progress.is_set():
                    time.sleep(2)
                    if not stop_progress.is_set():
                        sys.stdout.write('.')
                        sys.stdout.flush()
                        dot_count += 1
                        if dot_count % 5 == 0:  # Every 10 seconds
                            elapsed = int(time.time() - start_time)
                            print(f' [{elapsed}s]', end='', flush=True)
            
            progress_thread = threading.Thread(target=show_progress, daemon=True)
            progress_thread.start()
            
            try:
                tree = ElementTree.parse(str(xml_path))
                DrugBankService._shared_root = tree.getroot()
                
                stop_progress.set()
                progress_thread.join(timeout=1)
                
                parse_elapsed = time.time() - start_time
                print(f' ✅ ({parse_elapsed:.2f}s)')
                
                # Cache all drugs
                print("📦 Caching all drugs...", end='', flush=True)
                cache_start = time.time()
                self._cache_all_drugs()
                cache_elapsed = time.time() - cache_start
                print(f' ✅ ({cache_elapsed:.2f}s)')
                
                total_elapsed = time.time() - start_time
                print(f'{"="*70}')
                print(f'✅ DATABASE LOADED SUCCESSFULLY!')
                print(f'⏱️  Total loading time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)')
                print(f'📊 Total drugs cached: {len(DrugBankService._shared_drugs_cache):,}')
                print(f'💾 Memory: XML tree + drug cache ready')
                print(f'{"="*70}\n')
                
                DrugBankService._is_loaded = True
                return DrugBankService._shared_root
            except Exception as e:
                stop_progress.set()
                progress_thread.join(timeout=1)
                print(f'\n❌ Error loading database: {e}\n')
                raise
    
    def _cache_all_drugs(self):
        """Cache all drugs with essential info for instant filtering"""
        if DrugBankService._shared_drugs_cache is not None:
            return  # Already cached
        
        drugs = []
        for drug in DrugBankService._shared_root.findall('db:drug', self.namespace):
            drugbank_id_elem = drug.find('db:drugbank-id[@primary="true"]', self.namespace)
            drugbank_id = drugbank_id_elem.text if drugbank_id_elem is not None else 'N/A'
            
            name = self._get_text(drug, 'db:name')
            if not name:
                continue
            
            # Get drug type
            drug_type = drug.get('type', 'small molecule')
            
            # Get synonyms
            synonyms = []
            synonyms_elem = drug.find('db:synonyms', self.namespace)
            if synonyms_elem is not None:
                for synonym in synonyms_elem.findall('db:synonym', self.namespace):
                    if synonym.text:
                        synonyms.append(synonym.text)
            
            # Get description
            description = self._get_text(drug, 'db:description')
            
            # Get indication
            indication = self._get_text(drug, 'db:indication')
            
            # Get categories
            categories = []
            categories_elem = drug.find('db:categories', self.namespace)
            if categories_elem is not None:
                for cat in categories_elem.findall('db:category', self.namespace):
                    cat_name = self._get_text(cat, 'db:category')
                    if cat_name:
                        categories.append(cat_name)
            
            drugs.append({
                'name': name,
                'drugbank_id': drugbank_id,
                'type': drug_type,
                'synonyms': synonyms[:3],  # First 3 synonyms
                'description': description[:200] if description else '',  # First 200 chars
                'indication': indication[:200] if indication else '',
                'categories': categories[:5]  # First 5 categories
            })
        
        DrugBankService._shared_drugs_cache = drugs
    
    def get_all_drugs(self):
        """Get all cached drugs (triggers loading if not loaded)"""
        # Ensure root is loaded (which also caches drugs)
        _ = self.root
        return DrugBankService._shared_drugs_cache if DrugBankService._shared_drugs_cache else []
    
    def search_drugs(self, query):
        """Search for drugs by name (uses shared singleton cache)"""
        try:
            # Ensure database is loaded
            _ = self.root
            
            query_lower = query.lower()
            results = []
            
            for drug in DrugBankService._shared_root.findall('db:drug', self.namespace):
                # Get drug name
                name_elem = drug.find('db:name', self.namespace)
                if name_elem is None:
                    continue
                
                drug_name = name_elem.text or ''
                
                # Check if query matches name
                if query_lower in drug_name.lower():
                    drugbank_id_elem = drug.find('db:drugbank-id[@primary="true"]', self.namespace)
                    drugbank_id = drugbank_id_elem.text if drugbank_id_elem is not None else 'N/A'
                    
                    # Get synonyms for better matching
                    synonyms = []
                    synonyms_elem = drug.find('db:synonyms', self.namespace)
                    if synonyms_elem is not None:
                        for synonym in synonyms_elem.findall('db:synonym', self.namespace):
                            if synonym.text:
                                synonyms.append(synonym.text)
                    
                    # Get drug type
                    drug_type = drug.get('type', 'small molecule')
                    
                    results.append({
                        'name': drug_name,
                        'drugbank_id': drugbank_id,
                        'prescribable_name': drug_name,
                        'synonyms': synonyms[:3],  # First 3 synonyms
                        'type': drug_type
                    })
                    
                    if len(results) >= 20:  # Limit results
                        break
            
            return {
                'success': True,
                'data': results
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_drug_details(self, drugbank_id):
        """Get detailed information about a specific drug"""
        try:
            # Find drug by DrugBank ID
            drug = None
            for d in DrugBankService._shared_root.findall('db:drug', self.namespace):
                db_id = d.find('db:drugbank-id[@primary="true"]', self.namespace)
                if db_id is not None and db_id.text == drugbank_id:
                    drug = d
                    break
            
            if drug is None:
                return {
                    'success': False,
                    'error': 'Drug not found'
                }
            
            # Extract drug information
            name = self._get_text(drug, 'db:name')
            description = self._get_text(drug, 'db:description')
            indication = self._get_text(drug, 'db:indication')
            cas_number = self._get_text(drug, 'db:cas-number')
            
            # Get categories
            categories = []
            categories_elem = drug.find('db:categories', self.namespace)
            if categories_elem is not None:
                for cat in categories_elem.findall('db:category', self.namespace):
                    cat_name = self._get_text(cat, 'db:category')
                    if cat_name:
                        categories.append({'name': cat_name})
            
            return {
                'success': True,
                'data': {
                    'drugbank_id': drugbank_id,
                    'name': name,
                    'description': description,
                    'indication': indication,
                    'cas_number': cas_number,
                    'categories': categories
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_drug_interactions(self, drugbank_id_1, drugbank_id_2):
        """Check for interactions between two drugs"""
        try:
            interactions = []
            
            # Find first drug
            drug1 = None
            for d in DrugBankService._shared_root.findall('db:drug', self.namespace):
                db_id = d.find('db:drugbank-id[@primary="true"]', self.namespace)
                if db_id is not None and db_id.text == drugbank_id_1:
                    drug1 = d
                    break
            
            if drug1 is None:
                return {
                    'success': False,
                    'error': f'Drug {drugbank_id_1} not found'
                }
            
            # Get drug1 name
            drug1_name = self._get_text(drug1, 'db:name')
            
            # Check drug1's interactions for drug2
            interactions_elem = drug1.find('db:drug-interactions', self.namespace)
            if interactions_elem is not None:
                for interaction in interactions_elem.findall('db:drug-interaction', self.namespace):
                    interacting_id_elem = interaction.find('db:drugbank-id', self.namespace)
                    if interacting_id_elem is not None and interacting_id_elem.text == drugbank_id_2:
                        description = self._get_text(interaction, 'db:description')
                        drug2_name = self._get_text(interaction, 'db:name')
                        
                        # Determine severity based on keywords in description
                        severity = 'minor'
                        if description:
                            desc_lower = description.lower()
                            if any(word in desc_lower for word in ['severe', 'serious', 'major']):
                                severity = 'major'
                            elif any(word in desc_lower for word in ['moderate', 'caution']):
                                severity = 'moderate'
                        
                        interactions.append({
                            'drug1': drug1_name,
                            'drug2': drug2_name,
                            'description': description,
                            'severity': severity
                        })
            
            # Also check the reverse (drug2's interactions with drug1)
            drug2 = None
            for d in DrugBankService._shared_root.findall('db:drug', self.namespace):
                db_id = d.find('db:drugbank-id[@primary="true"]', self.namespace)
                if db_id is not None and db_id.text == drugbank_id_2:
                    drug2 = d
                    break
            
            if drug2 is not None:
                drug2_name = self._get_text(drug2, 'db:name')
                interactions_elem = drug2.find('db:drug-interactions', self.namespace)
                if interactions_elem is not None:
                    for interaction in interactions_elem.findall('db:drug-interaction', self.namespace):
                        interacting_id_elem = interaction.find('db:drugbank-id', self.namespace)
                        if interacting_id_elem is not None and interacting_id_elem.text == drugbank_id_1:
                            # Check if we already have this interaction
                            description = self._get_text(interaction, 'db:description')
                            if not any(i['description'] == description for i in interactions):
                                # Determine severity
                                severity = 'minor'
                                if description:
                                    desc_lower = description.lower()
                                    if any(word in desc_lower for word in ['severe', 'serious', 'major']):
                                        severity = 'major'
                                    elif any(word in desc_lower for word in ['moderate', 'caution']):
                                        severity = 'moderate'
                                
                                interactions.append({
                                    'drug1': drug2_name,
                                    'drug2': drug1_name,
                                    'description': description,
                                    'severity': severity
                                })
            
            return {
                'success': True,
                'data': interactions,
                'total': len(interactions)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_text(self, element, tag):
        """Helper method to safely get text from XML element"""
        elem = element.find(tag, self.namespace)
        return elem.text if elem is not None and elem.text else ''

