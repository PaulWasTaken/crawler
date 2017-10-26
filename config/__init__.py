import py

STORAGE_THRESHOLD = 10000000  # Size in bytes
VERIFY_SSL = False
PROJECT_ROOT = py.path.local(__file__).dirpath('..')
DB = PROJECT_ROOT.join('crawler-info.db')
