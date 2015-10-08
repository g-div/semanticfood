from setuptools import setup, find_packages
from codecs import open
from os import path
from pip.req import parse_requirements

readme = 'README.md'

requirements_file = 'requirements.txt'

requirements = [str(requirement.req) for requirement in parse_requirements(requirements_file)]

packages = find_packages()

with open(readme, 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='semanticfood',
    version='0.0.1',
    description='A web-platform to store, search and share cooking recipes semantically',
    long_description=readme,
    url='https://github.com/g-div/semanticfood',
    author='Giuseppe Di Vincenzo, Tim Eulitz',
    #author_email='',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='semantic food recipes',
    packages=packages,

    install_requires=requirements,

    package_data={'': [readme, requirements_file]},

    entry_points={
        'console_scripts': [
            'semanticfood=semanticfood.app:main',
        ],
    },
)