#!/usr/bin/env python3
"""
Script to rename all JSON files in versions/en/ to uppercase using git mv.
Executes the git mv commands directly.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Main entry point."""
    # Get the project root and versions/en directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    versions_en_dir = project_root / "versions" / "en"
    
    if not versions_en_dir.exists():
        print(f"Error: Directory {versions_en_dir} does not exist")
        sys.exit(1)
    
    # Get all JSON files
    json_files = list(versions_en_dir.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {versions_en_dir}")
        return
    
    print(f"Found {len(json_files)} JSON files")
    print(f"Project root: {project_root}")
    print()
    
    renamed_count = 0
    skipped_count = 0
    
    for file_path in sorted(json_files):
        filename = file_path.name
        stem = file_path.stem
        extension = file_path.suffix
        
        # Convert to uppercase
        new_name = stem.upper() + extension.lower()
        
        # Skip if target already exists (and is a different file)
        new_path = file_path.parent / new_name
        if new_path.exists() and new_path != file_path:
            print(f"SKIP: {filename} (target {new_name} already exists)")
            skipped_count += 1
            continue
        
        # If already uppercase, skip git mv (no change needed)
        if filename == new_name:
            print(f"OK: {filename} (already uppercase)")
            renamed_count += 1
            continue
        
        # Get relative paths from git root
        rel_old = file_path.relative_to(project_root)
        rel_new = new_path.relative_to(project_root)
        
        try:
            # Execute git mv
            result = subprocess.run(
                ['git', 'mv', str(rel_old), str(rel_new)],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                check=True
            )
            print(f"RENAMED: {filename} -> {new_name}")
            renamed_count += 1
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to rename {filename}: {e.stderr.strip()}")
            skipped_count += 1
        except Exception as e:
            print(f"ERROR: Exception renaming {filename}: {e}")
            skipped_count += 1
    
    print()
    print(f"Summary:")
    print(f"  Renamed: {renamed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(json_files)}")


if __name__ == "__main__":
    main()
