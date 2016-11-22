""" Jupytoc packaging instructions. """

from setuptools import setup, find_packages

__project__ = 'jupytoc'
__author__ = 'axelbellec'
__copyright__ = 'axelbellec'
__licence__ = 'MIT'
__version__ = '0.0.1'


README = 'README.md'
REQUIREMENTS = [
    'click==6.6'
]


def long_description():
    """ Insert README.md into the package. """
    try:
        with open(README) as readme_fd:
            return readme_fd.read()
    except IOError:
        return 'Failed to read ' + README


setup(
    name=__project__,
    version=__version__,
    description='A commmand-line interface to add or update TOC to Jupyter Notebooks',
    author=__author__,
    author_email='axel.bellec@outlook.fr',
    packages=find_packages(),
    long_description=long_description(),
    install_requires=REQUIREMENTS,
    keywords='jupytoc cli command line pip jupyter notebook tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    py_modules=['jupytoc'],
    entry_points={
        'console_scripts': [
            'jupytoc = jupytoc:cli'
        ]
    }
)
