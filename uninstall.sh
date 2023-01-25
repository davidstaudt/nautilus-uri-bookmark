#!/bin/bash

# Uninstall nautilus-url-shortcut

echo "Uninstalling nautilus-url-shortcut..."

# Uninstall Nautilus extension
rm ~/.local/share/nautilus-python/extensions/nautilus-url-shortcut.py

# Restart nautilus
echo "Restarting nautilus..."
nautilus -q

echo "Uninstallation Complete"
