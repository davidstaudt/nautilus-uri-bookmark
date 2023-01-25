# nautilus-url-shortcut
# 
# Save web URIs to a cross-platform shortcut file (.html) that can be launched to visit the URL
#
# Ensure the python-nautilus package is installed
# Place ~/.local/share/nautilus-python/extensions/, then restart Nautilus

# import re
import os
from gi import require_version
require_version('Gdk', '4.0')
from gi.repository import Nautilus, GObject, Gdk
from urllib.parse import urlparse

# if os.getenv('NAUTILUS_PYTHON_DEBUG') == 'misc':
#     import debugpy
#     debugpy.listen(5678)
#     print("Waiting for debugger attach")
#     debugpy.wait_for_client()

class UrlShortcutMenuProvider(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super().__init__()
        self.clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        self.inode = None

    def save_uri(self, menu, inode):

        self.inode = inode
        self.clipboard.read_text_async(None, self.read_text_async_cb)

    def read_text_async_cb(self, clipboard, result):

        text = clipboard.read_text_finish(result)
        try:
            link = urlparse(text)
        except:
            return []
        if link.scheme not in ['http','https']: return []

        fileText = f'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>URL Shortcut</title><meta http-equiv="refresh" charset="utf-8" content="0; url={link.geturl()}" /></head><body><p>Loading <a href="{link.geturl()}">{link.netloc}</a>...</p></body></html>'

        fileName = f'Link to {link.netloc}'
        fileName = ''.join( x for x in fileName if (x.isalnum() or x in ":&[]@._- ") )

        basePath = self.inode.get_location().get_path()
        if os.path.isfile(basePath): return
        if not os.path.exists(basePath): return
        instance = 0
        path = os.path.join(basePath, fileName+'.html')
        if os.path.exists(path):
            while True:
                instance += 1
                path = os.path.join(
                    basePath, f'{fileName}({str(instance)}).space')
                if not os.path.exists(path):
                    break
        with open(path, 'w') as file:
            file.write(fileText)

    def get_background_items(self, inode):

        item = Nautilus.MenuItem(
            name = 'nautilus_url_shortcut',
            label = 'Create URL shortcut',
            tip = 'Create shortcut file from clipboard web URI'
        )
        item.connect('activate', self.save_uri, inode)
        return [item]
