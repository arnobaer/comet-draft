from setuptools import setup, find_packages
import imp

version = imp.load_source('comet', 'comet/__init__.py').__version__

setup(
    name='comet',
    version=version,
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    packages=find_packages(),
    install_requires=[
        'bottle',
        'paste',
        'numpy',
    ],
    entry_points={
        'scripts': [
            'comet = comet.main:main',
        ],
    },
)
