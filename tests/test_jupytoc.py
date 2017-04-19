import sure

from jupytoc import core


def test_jupytoc_class_exists():
    core.should.have.property('Jupytoc')
