#!/usr/bin/env python3
"""
Script to rename all JSON files in versions/en/ to uppercase using git mv.
Example: git mv "American Standard Version.json" "AMERICAN STANDARD VERSION.json"
"""

import subprocess
import sys
from pathlib import Path

def git_rename_to_uppercase(directory: str):
    """Rename all JSON files in the directory to uppercase using git mv."""
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    if not dir_path.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)
    
    # Get all JSON files
    json_files = list(dir_path.glob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {directory}")
        return
    
    print(f"Found {len(json_files)} JSON files to rename")
    print()
    
    renamed_count = 0
    skipped_count = 0
    errors = []
    
    for file_path in sorted(json_files):
        # Get the filename without extension
        stem = file_path.stem
        extension = file_path.suffix  # .json
        
        # Convert to uppercase (keeping extension lowercase)
        new_name = stem.upper() + extension.lower()
        new_path = file_path.parent / new_name
        
        # Skip if already uppercase
        if file_path.name == new_name:
            print(f"SKIP: {file_path.name} (already uppercase)")
            skipped_count += 1
            continue
        
        # Skip if target already exists (and is different file)
        if new_path.exists() and new_path != file_path:
            print(f"SKIP: {file_path.name} (target {new_name} already exists)")
            skipped_count += 1
            continue
        
        try:
            # Use git mv to rename the file
            # Need to use relative paths from git root
            git_root = Path(directory).parent.parent  # versions/en -> versions -> root
            rel_old_path = file_path.relative_to(git_root)
            rel_new_path = new_path.relative_to(git_root)
            
            result = subprocess.run(
                ['git', 'mv', str(rel_old_path), str(rel_new_path)],
                cwd=str(git_root),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"RENAMED: {file_path.name} -> {new_name}")
                renamed_count += 1
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                print(f"ERROR: Failed to rename {file_path.name}: {error_msg}")
                errors.append((file_path.name, error_msg))
                skipped_count += 1
        except Exception as e:
            print(f"ERROR: Exception renaming {file_path.name}: {e}")
            errors.append((file_path.name, str(e)))
            skipped_count += 1
    
    print()
    print(f"Summary:")
    print(f"  Renamed: {renamed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(json_files)}")
    
    if errors:
        print()
        print(f"Errors ({len(errors)}):")
        for filename, error in errors:
            print(f"  {filename}: {error}")


def main():
    """Main entry point."""
    # Get the script directory and resolve the versions/en path
    script_dir = Path(__file__).parent
    versions_en_dir = (script_dir / ".." / "versions" / "en").resolve()
    
    print(f"Renaming files in: {versions_en_dir}")
    print("Using: git mv")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Cancelled.")
        sys.exit(0)
    
    print()
    git_rename_to_uppercase(str(versions_en_dir))


if __name__ == "__main__":
    main()
