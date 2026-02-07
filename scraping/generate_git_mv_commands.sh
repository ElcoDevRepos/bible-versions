#!/bin/bash
# Generate git mv commands to rename all files in versions/en/ to uppercase

cd "$(dirname "$0")/.." || exit 1

for file in versions/en/*.json; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        stem="${filename%.json}"
        extension="${filename##*.}"
        # Use tr to convert to uppercase (works on macOS)
        uppercase=$(echo "$stem" | tr '[:lower:]' '[:upper:]').${extension}
        
        # Only generate command if filename needs to be changed
        if [ "$filename" != "$uppercase" ]; then
            echo "git mv \"versions/en/$filename\" \"versions/en/$uppercase\""
        fi
    fi
done
