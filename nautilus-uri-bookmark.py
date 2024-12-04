# nautilus-uri-bookmark
#
# Save URIs to a file with a .uri extension that can be launched via xdg-open
# when the bookmark file is opened.
#
# Ensure the python-nautilus package is installed
# Place ~/.local/share/nautilus-python/extensions/, then restart Nautilus

from gi import require_version
require_version("Gdk", "4.0")
from gi.repository import Nautilus, GObject, Gdk

import os
from urllib.parse import urlparse

if os.getenv("NAUTILUS_PYTHON_DEBUG") == "misc":
    import debugpy

    debugpy.listen(5678)
    print("Waiting for debugger attach")
    debugpy.wait_for_client()

class UriBookmarkMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self.clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())

    def save_uri(self, menu, inode):

        def read_text_async_cb(clipboard, result):
            try:
                link = urlparse(clipboard.read_text_finish(result))
            except:
                return []

            fileName = f"{link.scheme.upper()}: {link.netloc}"

            basePath = inode.get_location().get_path()
            if not os.path.exists(basePath) or os.path.isfile(basePath):
                return
            instance = 0
            path = os.path.join(basePath, fileName + ".uri")
            while os.path.exists(path):
                instance += 1
                path = os.path.join(basePath, f"{fileName}({str(instance)}).uri")

            with open(path, "w") as file:
                file.write(link.geturl())

        self.clipboard.read_text_async(None, read_text_async_cb)

    def get_background_items(self, inode):

        item = Nautilus.MenuItem(
            name="nautilus_uri_bookmark",
            label="Create URI shortcut",
            tip="Create shortcut file from clipboard web URI",
        )
        item.connect("activate", self.save_uri, inode)
        
        return [item]
