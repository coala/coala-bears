import os

# Path to the bears directory
bears_root = os.path.dirname(__file__)

VERSION_FILE = os.path.join(bears_root, "VERSION")
with open(VERSION_FILE, 'r') as ver:
    VERSION = ver.readline().strip()
