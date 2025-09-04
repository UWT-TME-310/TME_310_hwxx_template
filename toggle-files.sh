#!/bin/bash

# Toggle file visibility in VS Code
# Run this script to show/hide instructor files

SETTINGS_FILE=".vscode/settings.json"
BACKUP_FILE=".vscode/settings.json.bak"

if grep -q '"files.exclude"' "$SETTINGS_FILE"; then
    echo "📁 Showing all files (instructor mode)..."
    # Backup current settings and remove files.exclude
    cp "$SETTINGS_FILE" "$BACKUP_FILE"
    # Remove the files.exclude block (lines containing files.exclude through the closing brace)
    sed -i '/^[[:space:]]*"files\.exclude"/,/^[[:space:]]*},*$/d' "$SETTINGS_FILE"
    echo "✅ All files now visible"
else
    echo "🔒 Hiding instructor files (student mode)..."
    if [ -f "$BACKUP_FILE" ]; then
        # Restore from backup
        cp "$BACKUP_FILE" "$SETTINGS_FILE"
        echo "✅ Files hidden for students"
    else
        echo "❌ No backup found. Please manually add files.exclude to settings.json"
    fi
fi

echo "🔄 Reload VS Code window to see changes"
