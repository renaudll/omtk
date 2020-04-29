#!/usr/bin/env python
"""
Python distutils definition
"""

from setuptools import setup, find_packages

setup(
    name="omtk",
    version="0.6.1",
    description="Lightweight open-source production tools for Maya",
    author="Renaud Lessard Larouche",
    author_email="sigmao@gmail.com",
    url="https://github.com/renaudll/maya-mock",
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    package_data={"omtk": ["compounds/*.ma"]},
    install_requires=["enum; python_version < '3.0'", "six", "mock"],
    include_package_data=True,
    extras_require={"test": ["pytest", "pytest-cov"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Multimedia :: Graphics",
    ],
)
