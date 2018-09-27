
PROJECT_NAME='pathcmd'
VERSION='1.1'

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
     long_description = f.read()

setup(
    name=PROJECT_NAME,
    version=VERSION,
    description='Cmd module with path completion',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kenta Suzuki',
    author_email='san.jose3993@gmail.com',
    packages=find_packages(),
    )
