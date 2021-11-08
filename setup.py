import os, platform
from setuptools import setup
req = """
flask 
pychromecast 
"""
if platform.system().lower() == "windows":
  os.system("pip install -r requirements.txt")
else:
  os.system("pip3 install -r requirements.txt")
requirements = []

requirements = req.splitlines()
setup(name="pihome", version="1.0.0", packages=["."], license="MIT", install_requires=requirements, classifiers=['Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed'])
