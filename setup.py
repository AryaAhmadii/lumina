from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="lumina",
    version="1",
    author="dwrrio",
    packages=find_packages(),
    install_requires = requirements,
)


# pip install -e .
