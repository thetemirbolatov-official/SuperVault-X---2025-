"""
setup.py для SuperVault X
Установка: python setup.py install
Публикация: python setup.py sdist bdist_wheel
            twine upload dist/*
"""

from setuptools import setup, find_packages
import os

# Читаем README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Читаем requirements
requirements = ["pycryptodome>=3.20.0"]

setup(
    name="supervaultx",
    version="5.0.0",
    author="thetemirbolatov",
    author_email="mirajestory@gmail.com",
    description="Super Vault X - Ultra secure file encryption with 10,000-line mega passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ftoop17/supervaultx",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
        "Topic :: System :: Filesystems",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Natural Language :: Russian",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "supervault=supervaultx:main",
            "svx=supervaultx:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ico", "*.txt", "*.md"],
    },
    keywords=[
        "encryption",
        "security",
        "cryptography",
        "file-protection",
        "vault",
        "password",
        "secure",
        "aes",
        "mega-password",
        "supervault",
        "thetemirbolatov",
    ],
    project_urls={
        "Bug Reports": "https://github.com/ftoop17/supervaultx/issues",
        "Source": "https://github.com/ftoop17/supervaultx",
        "Documentation": "https://github.com/ftoop17/supervaultx/wiki",
    },
)