import os
import platform

# Path to the bears directory
bears_root = os.path.dirname(__file__)

VERSION_FILE = os.path.join(bears_root, "VERSION")
with open(VERSION_FILE, 'r') as ver:
    VERSION = ver.readline().strip()

if platform.system() == 'Windows':  # pragma: no cover
    USER_DIR = os.path.join(os.getenv("APPDATA"), "coala")
else:
    USER_DIR = os.path.join(os.path.expanduser("~"), ".local", "coala")
