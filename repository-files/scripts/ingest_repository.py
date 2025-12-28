#!/usr/bin/env python3
"""
iLuminara-Core Repository Ingestion Engine
Generates comprehensive MDX documentation for 800+ files

This script:
1. Recursively scans the repository
2. Generates MDX documentation for each code file
3. Creates navigation structure
4. Validates completeness
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import ast
import hashlib

@dataclass
class FileMetadata:
    """Metadata for a single file"""
    path: str
    name: str
    extension: str
    size: int
    lines: int
    language: str
    category: str
    description: str
    functions: List[str]
    classes: List[str]
    imports: List[str]
    complexity: str
    sovereignty_level: str
    compliance_tags: List[str]

@dataclass
class NavigationNode:
    """Navigation structure node"""
    title: str
    path: str
    children: List['NavigationNode']
    icon: Optional[str] = None
    
class RepositoryIngestionEngine:
    """Main ingestion engine for iLuminara-Core"""
    
    # File extensions to process
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.sh': 'bash',
        '.md': 'markdown',
        '.sql': 'sql',
        '.dockerfile': 'docker',
        '.toml': 'toml'
    }
    
    # Directories to skip
    SKIP_DIRS = {
        '__pycache__', 'node_modules', '.git', '.github', 
        'venv', 'env', '.venv', 'dist', 'build', '.pytest_cache',
        '.mypy_cache', 'htmlcov', '.coverage', 'logs'
    }
    
    # Category mapping based on directory structure
    CATEGORY_MAP = {
        'governance_kernel': 'Governance kernel',
        'edge_node': 'Edge node',
        'cloud_oracle': 'Cloud oracle',
        'api': 'API reference',
        'tests': 'Testing',
        'scripts': 'Scripts',
        'config': 'Configuration',
        'docs': 'Documentation',
        'examples': 'Examples'
    }
    
    # Sovereignty levels
    SOVEREIGNTY_LEVELS = {
        'CRITICAL': ['governance_kernel', 'crypto_shredder', 'vector_ledger'],
        'HIGH': ['edge_node', 'ai_agents', 'sync_protocol'],
        'MEDIUM': ['api', 'dashboard', 'cloud_oracle'],
        'LOW': ['tests', 'scripts', 'examples']
    }
    
    def __init__(self, repo_path: str, output_path: str):
        self.repo_path = Path(repo_path)
        self.output_path = Path(output_path)
        self.files_processed = 0
        self.files_skipped = 0
        self.metadata_cache: Dict[str, FileMetadata] = {}
        
    def scan_repository(self) -> List[Path]:
        """Recursively scan repository for supported files"""
        files = []
        
        for root, dirs, filenames in os.walk(self.repo_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            
            for filename in filenames:
                file_path = Path(root) / filename
                ext = file_path.suffix.lower()
                
                if ext in self.SUPPORTED_EXTENSIONS:
                    files.append(file_path)
        
        return sorted(files)
    
    def extract_python_metadata(self, file_path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Extract functions, classes, and imports from Python file"""
        functions = []
        classes = []
        imports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return functions, classes, imports
    
    def calculate_complexity(self, file_path: Path) -> str:
        """Calculate file complexity based on size and structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            line_count = len(lines)
            
            if line_count < 50:
                return "LOW"
            elif line_count < 200:
                return "MEDIUM"
            elif line_count < 500:
                return "HIGH"
            else:
                return "VERY_HIGH"
        
        except Exception:
            return "UNKNOWN"
    
    def determine_sovereignty_level(self, file_path: Path) -> str:
        """Determine sovereignty level based on file location"""
        path_str = str(file_path)
        
        for level, keywords in self.SOVEREIGNTY_LEVELS.items():
            if any(keyword in path_str for keyword in keywords):
                return level
        
        return "LOW"
    
    def extract_compliance_tags(self, file_path: Path) -> List[str]:
        """Extract compliance tags from file content"""
        tags = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Search for compliance mentions
            compliance_patterns = [
                r'GDPR', r'HIPAA', r'KDPA', r'POPIA', r'PIPEDA',
                r'ISO 27001', r'SOC 2', r'NIST', r'EU AI Act'
            ]
            
            for pattern in compliance_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    tags.append(pattern)
        
        except Exception:
            pass
        
        return list(set(tags))
    
    def generate_file_metadata(self, file_path: Path) -> FileMetadata:
        """Generate comprehensive metadata for a file"""
        rel_path = file_path.relative_to(self.repo_path)
        ext = file_path.suffix.lower()
        language = self.SUPPORTED_EXTENSIONS.get(ext, 'text')
        
        # Determine category
        category = "Other"
        for key, value in self.CATEGORY_MAP.items():
            if key in str(rel_path):
                category = value
                break
        
        # Extract Python-specific metadata
        functions, classes, imports = [], [], []
        if ext == '.py':
            functions, classes, imports = self.extract_python_metadata(file_path)
        
        # Calculate metrics
        try:
            size = file_path.stat().st_size
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
        except Exception:
            size = 0
            lines = 0
        
        # Generate description
        description = self.generate_description(file_path, functions, classes)
        
        return FileMetadata(
            path=str(rel_path),
            name=file_path.name,
            extension=ext,
            size=size,
            lines=lines,
            language=language,
            category=category,
            description=description,
            functions=functions[:10],  # Limit to top 10
            classes=classes[:10],
            imports=imports[:10],
            complexity=self.calculate_complexity(file_path),
            sovereignty_level=self.determine_sovereignty_level(file_path),
            compliance_tags=self.extract_compliance_tags(file_path)
        )
    
    def generate_description(self, file_path: Path, functions: List[str], classes: List[str]) -> str:
        """Generate a description for the file"""
        name = file_path.stem
        
        # Try to extract docstring
        if file_path.suffix == '.py':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    docstring = ast.get_docstring(tree)
                    if docstring:
                        return docstring.split('\n')[0][:200]
            except Exception:
                pass
        
        # Generate based on content
        if classes:
            return f"Implements {', '.join(classes[:3])} for {name}"
        elif functions:
            return f"Provides {', '.join(functions[:3])} functionality"
        else:
            return f"Configuration and utilities for {name}"
    
    def generate_mdx_content(self, metadata: FileMetadata, file_path: Path) -> str:
        """Generate MDX documentation for a file"""
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = "# Unable to read file content"
        
        # Build MDX
        mdx = f"""---
title: {metadata.name}
description: {metadata.description}
---

## Overview

**File:** `{metadata.path}`  
**Language:** {metadata.language}  
**Category:** {metadata.category}  
**Lines:** {metadata.lines}  
**Complexity:** {metadata.complexity}  
**Sovereignty Level:** {metadata.sovereignty_level}

{metadata.description}

"""
        
        # Add compliance tags
        if metadata.compliance_tags:
            mdx += f"""## Compliance

This file implements or references the following compliance frameworks:

"""
            for tag in metadata.compliance_tags:
                mdx += f"- **{tag}**\n"
            mdx += "\n"
        
        # Add classes
        if metadata.classes:
            mdx += f"""## Classes

"""
            for cls in metadata.classes:
                mdx += f"### `{cls}`\n\n"
            mdx += "\n"
        
        # Add functions
        if metadata.functions:
            mdx += f"""## Functions

"""
            for func in metadata.functions:
                mdx += f"- `{func}()`\n"
            mdx += "\n"
        
        # Add imports
        if metadata.imports:
            mdx += f"""## Dependencies

```python
"""
            for imp in metadata.imports[:20]:
                mdx += f"import {imp}\n"
            mdx += "```\n\n"
        
        # Add source code
        mdx += f"""## Source code

```{metadata.language}
{content}
```

## File metadata

| Property | Value |
|----------|-------|
| Path | `{metadata.path}` |
| Size | {metadata.size} bytes |
| Lines | {metadata.lines} |
| Language | {metadata.language} |
| Complexity | {metadata.complexity} |
| Sovereignty | {metadata.sovereignty_level} |
"""
        
        return mdx
    
    def generate_navigation_structure(self, files: List[FileMetadata]) -> Dict:
        """Generate navigation structure for docs.json"""
        
        # Group by category
        categories = {}
        for file in files:
            if file.category not in categories:
                categories[file.category] = []
            categories[file.category].append(file)
        
        # Build navigation
        navigation = []
        
        for category, category_files in sorted(categories.items()):
            # Group by subdirectory
            subdirs = {}
            for file in category_files:
                parts = Path(file.path).parts
                if len(parts) > 1:
                    subdir = parts[0]
                    if subdir not in subdirs:
                        subdirs[subdir] = []
                    subdirs[subdir].append(file)
                else:
                    if 'root' not in subdirs:
                        subdirs['root'] = []
                    subdirs['root'].append(file)
            
            # Create group
            group_pages = []
            for subdir, subdir_files in sorted(subdirs.items()):
                for file in sorted(subdir_files, key=lambda x: x.name):
                    # Convert path to doc path
                    doc_path = f"reference/{file.path.replace(file.extension, '')}"
                    group_pages.append(doc_path)
            
            navigation.append({
                "group": category,
                "pages": group_pages[:50]  # Limit to 50 per group
            })
        
        return navigation
    
    def process_repository(self):
        """Main processing function"""
        print("🚀 iLuminara-Core Repository Ingestion Engine")
        print("=" * 60)
        
        # Scan repository
        print("\n📂 Scanning repository...")
        files = self.scan_repository()
        print(f"   Found {len(files)} files to process")
        
        # Process each file
        print("\n⚙️  Processing files...")
        all_metadata = []
        
        for i, file_path in enumerate(files, 1):
            try:
                # Generate metadata
                metadata = self.generate_file_metadata(file_path)
                all_metadata.append(metadata)
                
                # Generate MDX
                mdx_content = self.generate_mdx_content(metadata, file_path)
                
                # Write MDX file
                output_file = self.output_path / "reference" / metadata.path.replace(metadata.extension, '.mdx')
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(mdx_content)
                
                self.files_processed += 1
                
                if i % 50 == 0:
                    print(f"   Processed {i}/{len(files)} files...")
            
            except Exception as e:
                print(f"   ⚠️  Error processing {file_path}: {e}")
                self.files_skipped += 1
        
        print(f"\n✅ Processed {self.files_processed} files")
        print(f"⚠️  Skipped {self.files_skipped} files")
        
        # Generate navigation
        print("\n🗺️  Generating navigation structure...")
        navigation = self.generate_navigation_structure(all_metadata)
        
        # Write navigation JSON
        nav_file = self.output_path / "navigation_reference.json"
        with open(nav_file, 'w', encoding='utf-8') as f:
            json.dump(navigation, f, indent=2)
        
        print(f"   Navigation written to {nav_file}")
        
        # Generate metadata index
        print("\n📊 Generating metadata index...")
        metadata_file = self.output_path / "metadata_index.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(m) for m in all_metadata], f, indent=2)
        
        print(f"   Metadata written to {metadata_file}")
        
        # Generate summary
        self.generate_summary(all_metadata)
    
    def generate_summary(self, metadata: List[FileMetadata]):
        """Generate ingestion summary"""
        print("\n" + "=" * 60)
        print("📈 INGESTION SUMMARY")
        print("=" * 60)
        
        # By category
        categories = {}
        for m in metadata:
            categories[m.category] = categories.get(m.category, 0) + 1
        
        print("\n📁 Files by category:")
        for category, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"   {category:30} {count:4} files")
        
        # By language
        languages = {}
        for m in metadata:
            languages[m.language] = languages.get(m.language, 0) + 1
        
        print("\n💻 Files by language:")
        for language, count in sorted(languages.items(), key=lambda x: -x[1]):
            print(f"   {language:30} {count:4} files")
        
        # By sovereignty level
        sovereignty = {}
        for m in metadata:
            sovereignty[m.sovereignty_level] = sovereignty.get(m.sovereignty_level, 0) + 1
        
        print("\n🛡️  Files by sovereignty level:")
        for level, count in sorted(sovereignty.items(), key=lambda x: -x[1]):
            print(f"   {level:30} {count:4} files")
        
        # Total lines
        total_lines = sum(m.lines for m in metadata)
        print(f"\n📊 Total lines of code: {total_lines:,}")
        
        print("\n✅ Ingestion complete!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python ingest_repository.py <repo_path> <output_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    output_path = sys.argv[2]
    
    engine = RepositoryIngestionEngine(repo_path, output_path)
    engine.process_repository()
