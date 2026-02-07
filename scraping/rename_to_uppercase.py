#!/usr/bin/env python3
"""
Script to rename all JSON files in versions/en/ to uppercase.
Example: "American Standard Version.json" -> "AMERICAN STANDARD VERSION.json"
"""

import os
from pathlib import Path
import sys

def rename_files_to_uppercase(directory: str):
    """Rename all JSON files in the directory to uppercase names."""
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
    deleted_count = 0
    skipped_count = 0
    
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
        
        # Check if target file already exists
        if new_path.exists() and new_path != file_path:
            # Uppercase version already exists, delete the title case version
            try:
                # Optionally verify files are the same (for safety)
                # For now, just delete the title case version
                file_path.unlink()
                print(f"DELETED: {file_path.name} (uppercase version already exists: {new_name})")
                deleted_count += 1
            except Exception as e:
                print(f"ERROR: Failed to delete {file_path.name}: {e}")
                skipped_count += 1
            continue
        
        try:
            # Rename the file
            file_path.rename(new_path)
            print(f"RENAMED: {file_path.name} -> {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"ERROR: Failed to rename {file_path.name}: {e}")
            skipped_count += 1
    
    print()
    print(f"Summary:")
    print(f"  Renamed: {renamed_count}")
    print(f"  Deleted (duplicate): {deleted_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(json_files)}")


def main():
    """Main entry point."""
    # Get the script directory and resolve the versions/en path
    script_dir = Path(__file__).parent
    versions_en_dir = (script_dir / ".." / "versions" / "en").resolve()
    
    print(f"Renaming files in: {versions_en_dir}")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Cancelled.")
        sys.exit(0)
    
    print()
    rename_files_to_uppercase(str(versions_en_dir))


if __name__ == "__main__":
    main()
