from distutils.core import setup
import py2exe

setup(
    options={'py2exe': {
        'excludes': [],
        'optimize': 2,
        'compressed': False}},
    console=['main.py'],
    zipfile=None,
)