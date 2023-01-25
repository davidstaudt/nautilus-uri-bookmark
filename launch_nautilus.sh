#!/bin/bash
cp nautilus-url-shortcut.py ~/.local/share/nautilus-python/extensions; killall nautilus; env NAUTILUS_PYTHON_DEBUG=misc nautilus &