#!usr/bin/env python3

import setuptools

long_description = open("README.md", encoding="utf-8").read()

setuptools.setup(
    name="dsf-python",
    version="3.4.5",
    description="Python interface to access DuetSoftwareFramework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Duet3D/dsf-python",
    author="Duet3D Ltd.",
    author_email="pkg@duet3d.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="Duet3D, DuetSoftwareFramework, DSF, dsf-python",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7, <4",
    extras_require={
        "dev": [
            "sphinx",
            "tox",
        ],
    },
    project_urls={
        "Duet3D Support": "https://forum.duet3d.com/",
        "Bug Reports": "https://github.com/Duet3D/dsf-python/issues",
        "Source": "https://github.com/Duet3D/dsf-python/",
    },
)
