from setuptools import setup, find_packages
from os import path
import re

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSIONFILE = "bot/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
    name='defichain_donation_bot',
    version=verstr,
    author='Adrian Schnell',
    author_email='mail@adrian-schnell.consumer_key',
    license='LICENSE.md',
    description='This script is designed for tweeting new incoming funds on a predefined DFI address.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['psutil', 'requests', 'tweepy'],
    python_requires='>2.7'
)