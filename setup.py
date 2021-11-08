import os, platform
from setuptools import setup
if platform.system().lower() == "windows":
req = """
flask 
pychromecast 
"""

  os.system("pip install -r requirements.txt")
else:
  os.system("pip3 install -r requirements.txt")
requirements = []

requirements = req.splitlines()
setup(name="pihome", version="1.0.0", packages=["."], license="MIT", install_requires=requirements, classifiers=['Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: All',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: MUSIC',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed'])
