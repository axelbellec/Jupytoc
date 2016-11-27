import pytest
import click
from click.testing import CliRunner
import sure

import jupytoc


@pytest.fixture
def sample_notebooks():
    return tuple('notebook_{}.ipynb'.format(i) for i in range(3))


@pytest.fixture
def sample_notebook(sample_notebooks):
    return sample_notebooks[0]


def test_tuple_without_item_success(sample_notebooks, sample_notebook):
    jupytoc.util.should.have.property('get_tuple_without_item')
    notebooks = jupytoc.util.get_tuple_without_item(sample_notebooks, sample_notebook)
    assert sample_notebook not in notebooks


def test_empty_file(sample_notebook):
    jupytoc.util.should.have.property('is_file_not_empty')
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(sample_notebook, 'w') as f:
            f.write('')
        assert jupytoc.util.is_file_not_empty(sample_notebook) == False


def test_not_empty_file(sample_notebook):
    jupytoc.util.should.have.property('is_file_not_empty')
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open(sample_notebook, 'w') as f:
            f.write('Some content')
        assert jupytoc.util.is_file_not_empty(sample_notebook) == True
