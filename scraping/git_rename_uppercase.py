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
        
        # Get relative paths from git root
        rel_old = file_path.relative_to(project_root)
        rel_new = new_path.relative_to(project_root)
        rel_temp = versions_en_dir.relative_to(project_root) / "temp.json"
        
        try:
            # Two-step rename for case-insensitive filesystems with commits
            # Step 1: Rename to temporary file
            print(f"Step 1: Renaming {filename} to temp.json...")
            result1 = subprocess.run(
                ['git', 'mv', str(rel_old), str(rel_temp)],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                check=True
            )
            
            # Commit the temp rename
            result_commit1 = subprocess.run(
                ['git', 'commit', '-m', 'Temp rename to force case change'],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  Committed temp rename")
            
            # Step 2: Rename from temp to uppercase
            print(f"Step 2: Renaming temp.json to {new_name}...")
            result2 = subprocess.run(
                ['git', 'mv', str(rel_temp), str(rel_new)],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                check=True
            )
            
            # Commit the final rename
            result_commit2 = subprocess.run(
                ['git', 'commit', '-m', 'Rename file to uppercase'],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  Committed final rename")
            
            print(f"RENAMED: {filename} -> {new_name}")
            renamed_count += 1
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to rename {filename}: {e.stderr.strip()}")
            # Try to clean up temp file if it exists
            temp_path = project_root / rel_temp
            if temp_path.exists():
                try:
                    subprocess.run(['git', 'mv', str(rel_temp), str(rel_old)], 
                                 cwd=str(project_root), capture_output=True)
                except:
                    pass
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
