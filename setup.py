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
        'appdirs',
        'python-statemachine',
        'numpy',
        'pyvisa',
        'pyvisa-py',
        'pyvisa-sim',
        'pyyaml',
        'bottle',
        'paste'
    ],
    entry_points={
        'scripts': [
            'comet = comet.main:main'
        ],
    },
    package_data={
        'comet': [
            'config/devices/*.yml',
            'assets/dist/index.html',
            'assets/dist/*.css',
            'assets/dist/*.js'
        ]
    },
    license="GPLv3",
    keywords="",
    platforms="any",
    classifiers=[]
)
