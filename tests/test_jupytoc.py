import click
import sure

from jupytoc import jupytoc


def test_jupytoc_class_exists():
    jupytoc.should.have.property('Jupytoc')
