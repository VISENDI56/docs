# iLuminara-Core Total Repository Ingestion Guide

## Overview

This guide explains how to execute the **Total Repository Ingestion Engine** to generate comprehensive documentation for all 800+ files in the iLuminara-Core repository.

## Why Total Ingestion?

Standard AI agents cannot generate 800 files in a single turn due to context limits. The solution is to use a Python script to programmatically:

1. **Crawl** your entire repository
2. **Generate** a documentation page for every single file
3. **Update** the docs.json navigation map to include them all

This bypasses AI summarization by physically creating documentation files for every component.

## Prerequisites

```bash
# Ensure Python 3.8+ is installed
python3 --version

# Navigate to repository root
cd /path/to/iLuminara-Core
```

## Step 1: Copy the Ingestion Engine

Copy `generate_full_docs.py` to your repository root:

```bash
# If you have the file locally
cp generate_full_docs.py /path/to/iLuminara-Core/

# Or create it directly
cat << 'EOF' > generate_full_docs.py
# [Paste the complete script content here]
EOF
```

## Step 2: Execute the Ingestion

```bash
# Make script executable
chmod +x generate_full_docs.py

# Run the ingestion engine
python3 generate_full_docs.py
```

### Expected Output

```
╔════════════════════════════════════════════════════════════╗
║   iLuminara-Core Total Repository Ingestion Engine        ║
║   Generating documentation for 800+ files                 ║
╚════════════════════════════════════════════════════════════╝

🔍 Scanning repository: .
✅ [1] governance_kernel/vector_ledger.py
✅ [2] governance_kernel/crypto_shredder.py
✅ [3] governance_kernel/ethical_engine.py
✅ [4] edge_node/frenasa_engine/voice_processor.py
...
✅ [800] infrastructure/aerial_6g/network_config.py

📝 Updating docs.json...
✅ Updated docs.json

╔════════════════════════════════════════════════════════════╗
║                    INGESTION COMPLETE                      ║
╚════════════════════════════════════════════════════════════╝

📊 Statistics:
   - Files documented: 800
   - Groups created: 45
   - Documentation root: reference/

🚀 Next steps:
   1. Review generated documentation in reference/
   2. Commit changes: git add . && git commit -m 'docs: total repository ingestion'
   3. Push to repository: git push

✅ The Sovereign Health Fortress documentation is complete.
```

## Step 3: Review Generated Documentation

The script creates a mirrored structure in the `reference/` directory:

```
reference/
├── governance_kernel/
│   ├── vector_ledger.mdx
│   ├── crypto_shredder.mdx
│   └── ethical_engine.mdx
├── edge_node/
│   ├── frenasa_engine/
│   │   ├── voice_processor.mdx
│   │   └── symptom_extractor.mdx
│   └── ai_agents/
│       ├── offline_agent.mdx
│       └── federated_learning.mdx
├── infrastructure/
│   ├── aerial_6g/
│   └── quantum_mesh/
└── ml_health/
    ├── bionemo/
    └── vertex_ai/
```

## Step 4: Commit and Push

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "docs: total repository ingestion (800+ files integrated)"

# Push to repository
git push origin main
```

## Step 5: Verify in Mintlify

After pushing, your Mintlify documentation will show:

1. **Code Reference** tab in the navigation
2. **45+ groups** organized by directory structure
3. **800+ pages** with complete technical reference

## What Gets Documented?

### File Types

- **Python** (`.py`) - Full docstrings, imports, compliance tags
- **JavaScript** (`.js`) - Module structure and dependencies
- **Shell Scripts** (`.sh`) - Execution context and usage
- **Configuration** (`.json`, `.yml`, `.yaml`) - Schema and options
- **Markdown** (`.md`) - Content and structure

### Ignored Directories

- `.git`, `.github`, `__pycache__`, `venv`, `node_modules`
- `docs`, `media`, `logo`, `.pytest_cache`, `.mypy_cache`
- `dist`, `build`, `*.egg-info`, `.vscode`, `.idea`

### Ignored Files

- `.DS_Store`, `package-lock.json`, `requirements.txt`
- `.gitignore`, `.env`, `.env.example`

## Generated Documentation Features

Each generated MDX file includes:

### 1. Metadata
- File path and category
- Language and syntax highlighting
- Nuclear IP Stack tags (if applicable)

### 2. Compliance Tags
- GDPR, KDPA, HIPAA, POPIA
- Geneva Convention, WHO IHR
- ISO 27001, SOC 2, NIST CSF

### 3. Source Code Reference
- GitHub link to source
- Import statements (Python)
- Dependencies

### 4. Architecture Context
- Integration with Governance Kernel
- Audit Trail connections
- Golden Thread data flows

### 5. Related Documentation
- Links to architecture guides
- API reference
- Deployment guides
- Security documentation

## Customization

### Modify File Extensions

Edit `ALLOWED_EXT` in `generate_full_docs.py`:

```python
ALLOWED_EXT = {".py", ".js", ".sh", ".json", ".yml", ".yaml", ".css", ".md", ".toml", ".rs", ".go"}
```

### Add Custom Compliance Tags

Edit `COMPLIANCE_TAGS`:

```python
COMPLIANCE_TAGS = {
    "vector_ledger.py": ["GDPR", "KDPA", "HIPAA", "POPIA"],
    "your_module.py": ["Custom Framework", "Industry Standard"],
}
```

### Modify Nuclear IP Components

Edit `NUCLEAR_IP_COMPONENTS`:

```python
NUCLEAR_IP_COMPONENTS = {
    "crypto_shredder.py": "IP-02",
    "your_innovation.py": "IP-07",
}
```

## Troubleshooting

### Issue: Script fails with encoding error

**Solution:** Ensure all files are UTF-8 encoded:

```bash
find . -name "*.py" -exec file {} \; | grep -v UTF-8
```

### Issue: Navigation not updating

**Solution:** Verify docs.json exists and is valid JSON:

```bash
python3 -m json.tool docs.json
```

### Issue: Too many files (>1000)

**Solution:** Run in batches by directory:

```python
# Modify REPO_ROOT in script
REPO_ROOT = "./governance_kernel"  # Process one directory at a time
```

## Advanced Usage

### Dry Run Mode

Test without creating files:

```python
# Add at top of generate_nav_structure()
DRY_RUN = True

if not DRY_RUN:
    with open(doc_full_path, 'w', encoding='utf-8') as f:
        f.write(mdx_content)
```

### Custom Templates

Modify `generate_mdx_content()` to use custom templates:

```python
def generate_mdx_content(file_path: str, rel_path: str) -> str:
    # Load custom template
    with open('templates/custom.mdx', 'r') as f:
        template = f.read()
    
    # Replace placeholders
    return template.format(
        filename=filename,
        path=rel_path,
        content=content
    )
```

### Parallel Processing

For large repositories, use multiprocessing:

```python
from multiprocessing import Pool

def process_file(file_info):
    # Process single file
    pass

with Pool(processes=8) as pool:
    pool.map(process_file, file_list)
```

## Integration with CI/CD

### GitHub Actions

```yaml
name: Update Documentation

on:
  push:
    branches: [ main ]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run ingestion
        run: python3 generate_full_docs.py
      - name: Commit changes
        run: |
          git config user.name "Documentation Bot"
          git config user.email "bot@iluminara.health"
          git add reference/ docs.json
          git commit -m "docs: auto-update from ingestion" || exit 0
          git push
```

## Validation

After ingestion, validate the documentation:

```bash
# Check file count
find reference/ -name "*.mdx" | wc -l

# Validate docs.json
python3 -m json.tool docs.json > /dev/null && echo "✅ Valid JSON"

# Check for broken links
grep -r "href=" reference/ | grep -v "http" | grep -v ".mdx"
```

## Maintenance

### Re-run Ingestion

Safe to re-run anytime - it will overwrite existing files:

```bash
python3 generate_full_docs.py
```

### Incremental Updates

For new files only, modify the script to check if MDX exists:

```python
if os.path.exists(doc_full_path):
    print(f"⏭️  Skipping existing: {rel_path}")
    continue
```

## Support

For issues or questions:

1. Check the [GitHub Issues](https://github.com/VISENDI56/iLuminara-Core/issues)
2. Review the [Documentation](https://docs.iluminara.health)
3. Contact: support@iluminara.health

## The Result

After ingestion, your Mintlify documentation will display:

- **Complete visibility** into all 800+ files
- **Organized structure** mirroring your repository
- **Compliance tags** for regulatory frameworks
- **Nuclear IP Stack** component identification
- **Architecture context** for every file
- **GitHub integration** with source links

**The Fortress is now fully documented. No file is hidden. No component is summarized away.**
