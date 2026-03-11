#!/usr/bin/env python

from setuptools import find_packages, setup

import feedr

setup(
    name="feedr",
    version=feedr.__version__,
    description="Terminal based RSS reader",
    author="Avikant Srivastava",
    author_email="contact@avikant.com",
    packages=find_packages(),
    package_data={"feedr": ["*.tcss"]},
    python_requires=">=3.11",
    install_requires=[
        "textual>=6.11.0",
        "aiohttp>=3.13.3",
        "click>=8.3.1",
        "rich>=14.2.0",
        "lorem-text>=3.0",
    ],
    extras_require={
        "dev": [
            "textual-dev>=1.8.0",
            "textual-serve>=1.1.3",
        ]
    },

)
