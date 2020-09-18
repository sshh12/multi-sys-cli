from setuptools import setup

setup(
    name="msc",
    version="0.1.0",
    packages=["msc"],
    entry_points={"console_scripts": ["msc = msc.__main__:main"]},
)