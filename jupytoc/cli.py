import os
import click

from jupytoc.util import EMOJI_WARNING, EMOJI_FAILURE, EMOJI_JUPYTOC
from jupytoc.util import find_notebooks_recursively, get_tuple_without_item, is_file_not_empty
from jupytoc.util import NOTEBOOK_EXTENSION


@click.command()
@click.argument('notebooks', nargs=-1, type=click.Path(exists=True))
@click.option('-R', '--recursive', default=False, is_flag=True, help='build TOC for all subdirectories recursively')
@click.option('-l', '--maxlevel', default=6, help='limit TOC entries to headings only up to the specified level')
@click.option('-t', '--title', default='', help='custom TOC title')
@click.option('-s', '--stdout', default=False, is_flag=True, help='print to stdout')
@click.option('-d', '--delete', default=False, is_flag=True, help='remove TOC from notebook file')
def cli(notebooks, recursive, maxlevel, title, stdout, delete):
    """ 
    A commmand-line interface to add/update/delete TOC 
    to Jupyter Notebooks.
    """
    if len(notebooks) == 0 and not recursive:
        click.secho(
            '\t{}  You must pass at least 1 notebook.'.format(EMOJI_FAILURE),
            fg='red')
    else:
        # If we give a path to a folder, we apply a recursive search
        # of all .ipynb files existing in it
        for notebook in notebooks:
            if os.path.isdir(notebook):
                notebooks += tuple(
                    ipynb for ipynb in os.listdir(notebook)
                    if ipynb.endswith(NOTEBOOK_EXTENSION)
                )
                notebooks = get_tuple_without_item(notebooks, notebook)

        if recursive:
            notebooks += tuple(find_notebooks_recursively())

        click.secho('{}  Jupytoc is building TOC for {} notebooks'.format(
            EMOJI_JUPYTOC, len(notebooks)), bold=True)

        if len(notebooks) == 0:
            click.secho('\t{}  No notebook found.'.format(EMOJI_WARNING), fg='yellow')

        for notebook in notebooks:
            if is_file_not_empty(notebook):
                Jupytoc(path=notebook, level=maxlevel, title=title, stdout=stdout, delete=delete)
            else:
                click.secho(
                    '\t{}  Empty file.\t[{}]'.format(
                        EMOJI_WARNING, notebook),
                    fg='yellow')

        click.echo('Done.')

if __name__ == '__main__':
    cli()
