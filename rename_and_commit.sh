#!/bin/bash

# Script to rename files to temp.json and back to force case change, then commit

cd "$(dirname "$0")/versions/en" || exit 1

# Loop through all .json files
for file in *.json; do
    if [ -f "$file" ]; then
        echo "Processing: $file"
        
        # Step 1: Rename to temp.json
        echo "  Renaming to temp.json..."
        git mv "$file" temp.json
        
        # Step 2: Rename back to original filename (same case)
        echo "  Renaming back to $file..."
        git mv temp.json "$file"
        
        # Step 3: Commit
        echo "  Committing..."
        git commit -m "Temp rename to force case change"
        
        echo "  Done!"
        echo ""
    fi
done

echo "All files processed!"
