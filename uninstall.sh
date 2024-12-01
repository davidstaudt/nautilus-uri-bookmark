#!/bin/bash

# Uninstall nautilus-uri-bookmark

echo "Uninstalling nautilus-uri-bookmark..."

# Uninstall Nautilus extension
rm ~/.local/share/nautilus-python/extensions/nautilus-uri-bookmark.py

# Restart nautilus
echo "Restarting nautilus..."
nautilus -q

echo "Uninstallation Complete"
