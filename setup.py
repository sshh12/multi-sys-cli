from setuptools import setup
import os

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="msc",
    version="0.1.0",
    packages=["msc"],
    entry_points={"console_scripts": ["msc = msc.__main__:main"]},
    install_requires=required,
)