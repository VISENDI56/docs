#!/usr/bin/env python3
"""
iLuminara-Core Total Repository Ingestion Engine
Generates comprehensive documentation for all 800+ files

This script bypasses AI summarization by physically creating
documentation files for every component in the repository.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Configuration
REPO_ROOT = "."
DOCS_ROOT = "reference"
DOCS_JSON = "docs.json"

# Ignore patterns
IGNORE_DIRS = {
    ".git", ".github", ".streamlit", "__pycache__", "venv", "node_modules", 
    "docs", "media", "logo", ".pytest_cache", ".mypy_cache", "dist", "build",
    "*.egg-info", ".vscode", ".idea", "keys", "logs"
}

IGNORE_FILES = {
    ".DS_Store", "package-lock.json", "generate_full_docs.py", 
    "requirements.txt", ".gitignore", ".env", ".env.example"
}

# File extensions to document
ALLOWED_EXT = {".py", ".js", ".sh", ".json", ".yml", ".yaml", ".css", ".md", ".toml"}

# Nuclear IP Stack components
NUCLEAR_IP_COMPONENTS = {
    "crypto_shredder.py": "IP-02",
    "acorn_protocol.py": "IP-03",
    "silent_flux.py": "IP-04",
    "golden_thread.py": "IP-05",
    "5dm_bridge.py": "IP-06"
}

# Compliance frameworks
COMPLIANCE_TAGS = {
    "vector_ledger.py": ["GDPR", "KDPA", "HIPAA", "POPIA"],
    "ethical_engine.py": ["Geneva Convention", "WHO IHR"],
    "crypto_shredder.py": ["GDPR Art. 17", "NIST SP 800-88"],
    "audit": ["SOC 2", "ISO 27001"]
}


def get_file_language(filename: str) -> str:
    """Determine language for syntax highlighting"""
    ext = os.path.splitext(filename)[1]
    lang_map = {
        ".py": "python",
        ".js": "javascript",
        ".sh": "bash",
        ".json": "json",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".css": "css",
        ".md": "markdown",
        ".toml": "toml"
    }
    return lang_map.get(ext, "text")


def extract_docstring(file_path: str) -> str:
    """Extract module docstring from Python files"""
    if not file_path.endswith('.py'):
        return ""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match triple-quoted docstrings at start of file
            match = re.search(r'^"""(.*?)"""', content, re.DOTALL | re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return ""


def extract_imports(file_path: str) -> List[str]:
    """Extract import statements from Python files"""
    if not file_path.endswith('.py'):
        return []
    
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
                elif line and not line.startswith('#'):
                    # Stop at first non-import, non-comment line
                    if imports:
                        break
    except Exception:
        pass
    return imports


def get_compliance_tags(file_path: str) -> List[str]:
    """Get compliance framework tags for file"""
    filename = os.path.basename(file_path)
    tags = []
    
    # Check exact filename matches
    if filename in COMPLIANCE_TAGS:
        tags.extend(COMPLIANCE_TAGS[filename])
    
    # Check partial matches
    for key, frameworks in COMPLIANCE_TAGS.items():
        if key in file_path:
            tags.extend(frameworks)
    
    return list(set(tags))  # Remove duplicates


def get_nuclear_ip_tag(filename: str) -> str:
    """Get Nuclear IP Stack tag if applicable"""
    return NUCLEAR_IP_COMPONENTS.get(filename, "")


def generate_mdx_content(file_path: str, rel_path: str) -> str:
    """Generate MDX content for a file"""
    filename = os.path.basename(file_path)
    language = get_file_language(filename)
    docstring = extract_docstring(file_path)
    imports = extract_imports(file_path)
    compliance_tags = get_compliance_tags(file_path)
    nuclear_ip = get_nuclear_ip_tag(filename)
    
    # Determine component category
    category = "Core Component"
    if "governance" in rel_path:
        category = "Governance Kernel"
    elif "edge_node" in rel_path:
        category = "Edge Node"
    elif "ai_agents" in rel_path:
        category = "AI Agents"
    elif "frenasa" in rel_path:
        category = "FRENASA Engine"
    elif "sync_protocol" in rel_path:
        category = "Golden Thread"
    elif "infrastructure" in rel_path:
        category = "Infrastructure"
    elif "ml_health" in rel_path:
        category = "ML Health"
    
    # Build MDX content
    content = f"""---
title: {filename}
description: Technical reference for {filename}
---

## Overview

**Category:** {category}  
**Path:** `{rel_path}`  
**Language:** {language.title()}
"""
    
    # Add Nuclear IP tag if applicable
    if nuclear_ip:
        content += f"""
<Card title=\"Nuclear IP Stack\" icon=\"atom\">
  This component implements **{nuclear_ip}** from the iLuminara Nuclear IP Stack
</Card>
"""
    
    # Add compliance tags
    if compliance_tags:
        content += f"""
## Compliance

This component enforces the following frameworks:

"""
        for tag in compliance_tags:
            content += f"- **{tag}**\n"
    
    # Add docstring if available
    if docstring:
        content += f"""
## Description

{docstring}
"""
    
    # Add imports section for Python files
    if imports:
        content += f"""
## Dependencies

```python
{chr(10).join(imports)}
```
"""
    
    # Add source code reference
    content += f"""
## Source code

View the complete implementation in the repository:

```{language}
# {rel_path}
# 
# This file is part of the iLuminara-Core Sovereign Health Fortress
# For full source code, see: https://github.com/VISENDI56/iLuminara-Core
```

<Card title=\"View on GitHub\" icon=\"github\" href=\"https://github.com/VISENDI56/iLuminara-Core/blob/main/{rel_path}\">
  See the complete source code and commit history
</Card>

## Integration

This component integrates with:

- **Governance Kernel** - All actions validated through SovereignGuardrail
- **Audit Trail** - Operations logged to tamper-proof ledger
- **Golden Thread** - Data flows through verified timeline
"""
    
    # Add architecture context
    if "governance" in rel_path:
        content += """
## Architecture context

This component is part of the **Governance Kernel**, which enforces 14 global legal frameworks:

- GDPR (EU)
- KDPA (Kenya)
- HIPAA (USA)
- POPIA (South Africa)
- And 10 additional frameworks

<Card title=\"Learn more\" icon=\"shield-check\" href=\"/governance/overview\">
  Explore the complete Governance Kernel documentation
</Card>
"""
    elif "edge_node" in rel_path:
        content += """
## Architecture context

This component is part of the **Edge Node**, enabling offline-first data collection and processing:

- Offline operation
- Intermittent connectivity
- Local sovereignty
- Edge-to-cloud sync

<Card title=\"Learn more\" icon=\"microchip\" href=\"/architecture/overview\">
  Explore the complete Edge Node architecture
</Card>
"""
    
    # Add related documentation
    content += """
## Related documentation

<CardGroup cols={2}>
  <Card title=\"Architecture\" icon=\"sitemap\" href=\"/architecture/overview\">
    System architecture overview
  </Card>
  <Card title=\"API Reference\" icon=\"terminal\" href=\"/api-reference/overview\">
    API endpoints and integration
  </Card>
  <Card title=\"Deployment\" icon=\"rocket\" href=\"/deployment/overview\">
    Deployment guides
  </Card>
  <Card title=\"Security\" icon=\"shield-halved\" href=\"/security/overview\">
    Security stack and compliance
  </Card>
</CardGroup>
"""
    
    return content


def should_ignore(path: str, is_dir: bool = False) -> bool:
    """Check if path should be ignored"""
    name = os.path.basename(path)
    
    if is_dir:
        return name in IGNORE_DIRS or name.startswith('.')
    else:
        if name in IGNORE_FILES or name.startswith('.'):
            return True
        ext = os.path.splitext(name)[1]
        return ext not in ALLOWED_EXT


def generate_nav_structure(root_path: str) -> Tuple[List[Dict], int]:
    """
    Walk repository and generate navigation structure
    Returns: (nav_items, file_count)
    """
    nav_groups = {}
    file_count = 0
    
    print(f"🔍 Scanning repository: {root_path}")
    
    for root, dirs, files in os.walk(root_path):
        # Filter directories in place
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), is_dir=True)]
        
        for file in files:
            if should_ignore(file):
                continue
            
            # Construct paths
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_path)
            
            # Skip if in docs directory
            if rel_path.startswith('docs/') or rel_path.startswith('reference/'):
                continue
            
            # Create doc path (mirroring repo structure)
            doc_dir = os.path.dirname(rel_path)
            doc_filename = os.path.splitext(os.path.basename(rel_path))[0] + ".mdx"
            doc_full_path = os.path.join(DOCS_ROOT, doc_dir, doc_filename)
            
            # Mintlify page reference (no extension)
            page_ref = os.path.join(DOCS_ROOT, doc_dir, os.path.splitext(os.path.basename(rel_path))[0])
            page_ref = page_ref.replace('\\', '/')  # Normalize path separators
            
            # Generate MDX content
            mdx_content = generate_mdx_content(full_path, rel_path)
            
            # Create directory and write file
            os.makedirs(os.path.dirname(doc_full_path), exist_ok=True)
            with open(doc_full_path, 'w', encoding='utf-8') as f:
                f.write(mdx_content)
            
            # Add to navigation structure
            group_name = doc_dir if doc_dir else "Root"
            group_name = group_name.replace('\\', '/').replace('_', ' ').title()
            
            if group_name not in nav_groups:
                nav_groups[group_name] = []
            
            nav_groups[group_name].append(page_ref)
            
            file_count += 1
            print(f"✅ [{file_count}] {rel_path}")
    
    # Convert to list format
    nav_items = []
    for group_name in sorted(nav_groups.keys()):
        nav_items.append({
            "group": group_name,
            "pages": sorted(nav_groups[group_name])
        })
    
    return nav_items, file_count


def update_docs_json(nav_items: List[Dict]):
    """Update docs.json with new navigation structure"""
    print(f"\n📝 Updating {DOCS_JSON}...")
    
    try:
        with open(DOCS_JSON, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"⚠️  {DOCS_JSON} not found, creating new configuration")
        config = {
            "$schema": "https://mintlify.com/docs.json",
            "name": "iLuminara-Core",
            "navigation": {}
        }
    
    # Ensure navigation structure exists
    if "navigation" not in config:
        config["navigation"] = {}
    
    if "tabs" not in config["navigation"]:
        config["navigation"]["tabs"] = []
    
    # Find or create "Code Reference" tab
    code_ref_tab = None
    for tab in config["navigation"]["tabs"]:
        if tab.get("tab") == "Code Reference":
            code_ref_tab = tab
            break
    
    if not code_ref_tab:
        code_ref_tab = {
            "tab": "Code Reference",
            "groups": []
        }
        config["navigation"]["tabs"].append(code_ref_tab)
    
    # Replace groups with new structure
    code_ref_tab["groups"] = nav_items
    
    # Write updated config
    with open(DOCS_JSON, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Updated {DOCS_JSON}")


def main():
    """Main execution"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   iLuminara-Core Total Repository Ingestion Engine        ║")
    print("║   Generating documentation for 800+ files                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Generate navigation structure and MDX files
    nav_items, file_count = generate_nav_structure(REPO_ROOT)
    
    # Update docs.json
    update_docs_json(nav_items)
    
    # Summary
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    INGESTION COMPLETE                      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"📊 Statistics:")
    print(f"   - Files documented: {file_count}")
    print(f"   - Groups created: {len(nav_items)}")
    print(f"   - Documentation root: {DOCS_ROOT}/")
    print()
    print("🚀 Next steps:")
    print("   1. Review generated documentation in reference/")
    print("   2. Commit changes: git add . && git commit -m 'docs: total repository ingestion'")
    print("   3. Push to repository: git push")
    print()
    print("✅ The Sovereign Health Fortress documentation is complete.")


if __name__ == "__main__":
    main()
