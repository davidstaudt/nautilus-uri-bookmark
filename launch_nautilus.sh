#!/bin/bash
cp nautilus-uri-bookmark.py ~/.local/share/nautilus-python/extensions/; killall nautilus; G_DEBUG="all" NAUTILUS_DEBUG="All" NAUTILUS_PYTHON_DEBUG="misc" nautilus &