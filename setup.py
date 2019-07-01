import os
import imp
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from pynpm import NPMPackage

version = imp.load_source('comet', 'comet/__init__.py').__version__

class BuildPyCommand(build_py):
    def run(self):
        pkg = NPMPackage(os.path.join('comet', 'assets', 'package.json'))
        pkg.install()
        pkg.run_script('build')
        build_py.run(self)

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
        'paste',
        'pynpm',
    ],
    cmdclass={
        'build_py': BuildPyCommand,
    },
    entry_points={
        'scripts': [
            'comet = comet.main:main',
        ],
    },
    package_data={
        'comet': [
            'config/devices/*.yml',
            'assets/dist/index.html',
            'assets/dist/*.css',
            'assets/dist/*.js',
        ]
    },
    license="GPLv3",
    keywords="",
    platforms="any",
    classifiers=[],
)
