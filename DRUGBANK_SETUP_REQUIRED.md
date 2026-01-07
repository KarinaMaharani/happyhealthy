# DrugBank XML Setup Instructions

## ⚠️ IMPORTANT: DrugBank XML File Not Included

The DrugBank XML database file (`full database.xml`) is **NOT included** in this repository because:
- File size: 1.8 GB (exceeds GitHub's 100 MB limit)
- Contains licensed data that shouldn't be publicly distributed
- Too large for version control

## 📥 How to Set Up DrugBank Database

### Step 1: Download DrugBank XML

1. **Create a DrugBank Account** (if you don't have one)
   - Go to: https://go.drugbank.com/
   - Click "Sign Up" and create a free account
   - Check your email for account confirmation

2. **Download the Full Database**
   - Login at: https://go.drugbank.com/releases/latest
   - Under "Downloads" section, find **"Full Database"**
   - Click to download: `drugbank_all_full_database.xml.zip` (~100MB compressed)
   - Extract the ZIP file to get `full database.xml` (~1.8GB)

### Step 2: Place the XML File

You have two options:

#### Option A: User Data Folder (Recommended)
```
C:\Users\<YourUsername>\.data\drugbank\full database.xml
```
or
```
C:\Users\<YourUsername>\.data\drugbank\drugbank.xml
```

Create the folder:
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.data\drugbank"
```

Then copy the XML file there.

#### Option B: Project Static Folder
```
static/full database.xml
```

Just place the file in the `static/` directory of this project.

### Step 3: Verify Setup

1. Start the Django server:
   ```powershell
   python manage.py runserver
   ```

2. Look for this message in the console:
   ```
   ============================================================
   📂 Loading DrugBank database from: [path to your XML file]
   ============================================================
   ✅ DATABASE LOADED SUCCESSFULLY!
   📊 Total drugs cached: 19,830
   ============================================================
   ```

3. Try searching for a drug (e.g., "aspirin") to confirm it works

### Step 4: First Load Performance

- **First time**: ~30-40 seconds to parse the XML and cache all drugs
- **After first load**: Instant search (data cached in memory)
- The cache persists while the server is running

## 🔍 File Detection

The app automatically checks these locations in order:
1. `C:\Users\<YourUsername>\.data\drugbank\drugbank.xml`
2. `C:\Users\<YourUsername>\.data\drugbank\full database.xml`
3. `<project>/data/drugbank.xml`
4. `<project>/data/full database.xml`
5. `<project>/static/drugbank.xml`
6. `<project>/static/full database.xml`

## ❓ Troubleshooting

### "DrugBank XML file not found"
- Make sure you downloaded and extracted the file
- Check the file is in one of the locations listed above
- Verify the filename matches exactly (case-sensitive on some systems)

### "Failed to load DrugBank database"
- The XML file might be corrupted - try re-downloading
- Make sure you have enough RAM (file is large)
- Check file permissions

### Where to get help
- DrugBank Support: support@drugbank.com
- DrugBank Documentation: https://docs.drugbank.com

## 📄 License Note

The DrugBank database is licensed by DrugBank and has specific terms of use. Make sure you comply with their license agreement when using this data.

---

**After setting up the XML file, you're ready to use Happy Healthy!** 🎉
