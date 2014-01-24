import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "omtk",
    version = "0.0.1",
    author = "Renaud Lessard Larouche",
    author_email = "sigmao@gmail.com",
    description = ("Open Maya Toolkit"),
    license = "BSD",
    keywords = "maya toolkit tools",
    url = "http://github.com/renaudll/omtk",
    packages=find_packages(),
    long_description="TODO",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha"
    ],
)