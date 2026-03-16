#!/usr/bin/env python

import re
from pathlib import Path

from setuptools import find_packages, setup

# Read version from __init__.py without importing
init_file = Path(__file__).parent / "__init__.py"
version = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_file.read_text()).group(1)

setup(
    name="feedr",
    version=version,
    description="Terminal based RSS reader",
    author="Avikant Srivastava",
    author_email="contact@avikant.com",
    packages=find_packages(),
    package_data={"feedr": ["*.tcss"]},
    python_requires=">=3.11",
    install_requires=[
        "textual>=6.11.0",
	"sqlalchemy>=2.0.48",
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
