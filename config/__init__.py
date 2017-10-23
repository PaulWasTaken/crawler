import py

VERIFY_SSL = False
PROJECT_ROOT = py.path.local(__file__).dirpath('..')
DB = PROJECT_ROOT.join('crawler-info.db')
