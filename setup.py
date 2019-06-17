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
        'psutil',
        'numpy',
        'pyvisa',
        'pyvisa-py',
        'pyvisa-sim',
        'pyyaml',
        'bottle',
        'paste',
        'jinja2',
    ],
    entry_points={
        'scripts': [
            'comet = comet.main:main',
        ],
    },
)
