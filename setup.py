from setuptools import setup, find_packages
import imp

with open("README.md") as f:
    readme = f.read()

with open("LICENSE.md") as f:
    license = f.read()

version = imp.load_source('comet.main', 'comet/__init__.py').__version__

setup(
    name="comet",
    version=version,
    description="",
    long_description=readme,
    author="",
    author_email="",
    url="",
    license=license,
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'PyQt5-sip',
        'PyYAML',
    ],
    entry_points={
        'gui_scripts': [
            'comet = comet.main:main'
        ]
    },
    package_data={
        "comet": [
            "config/setups/*/settigns.yml",
        ]
    }
)
