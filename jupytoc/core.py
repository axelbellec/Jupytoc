import click
import json


from jupytoc.constants import EMOJI_SUCESS, EMOJI_WARNING, EMOJI_FAILURE


class Jupytoc(object):

    def __init__(self, path, level, title, stdout, delete):
        self.notebook_path = path
        self.credits = '<!-- Table of Contents generated by Jupytoc -->'
        self.maxlevel = level
        self.title = title if title != '' else '**Table of Contents**'
        self.stdout = stdout
        self.delete = delete
        self.compute_toc()

    def read_notebook_content(self):
        with open(self.notebook_path, 'r') as file:
            return json.load(file)

    def find_existing_toc(self, ipynb):
        for i, cell in enumerate(ipynb['cells']):
            if cell['cell_type'] == 'markdown' and self.credits + '\n' in cell['source']:
                return (True, i)
        return (False, None)

    def get_markdown_cells(self, ipynb):
        return [cell for cell in ipynb['cells'] if cell['cell_type'] == 'markdown']

    def get_markdown_lines(self, markdown_cells):
        return [[line for line in cell['source']] for cell in markdown_cells]

    def get_headers(self, markdown_lines):
        for lines in markdown_lines:
            for line in lines:
                stripped_right = line.rstrip('#')
                stripped_both = stripped_right.lstrip('#')
                stripped_wspace = stripped_both.strip()
                level = len(stripped_right) - len(stripped_both)
                link_anchor = lambda header: '#{}'.format(header.replace(' ', '-'))
                if level > 0 and level <= self.maxlevel:
                    yield (level, stripped_wspace, link_anchor(stripped_wspace))

    def build_toc(self, headers):
        return [self.credits + '\n'] + [self.title + '\n'] + ['{nb_spaces}- [{title}]({link})\n'.format(
            nb_spaces=' ' * 2 * (level - 1),
            title=title,
            link=link_anchor
        ) for level, title, link_anchor in headers]

    def write_toc(self, ipynb, toc, update_toc, position):
        markdown_cell = lambda toc: {
            'cell_type': 'markdown',
            'metadata': {},
            'source': toc
        }

        if update_toc:
            click.secho('\t{}  TOC updated.\t[{}]'.format(
                EMOJI_SUCESS, self.notebook_path), fg='green')
            ipynb['cells'][position] = markdown_cell(toc)
        else:
            ipynb['cells'].insert(0, markdown_cell(toc))
            click.secho('\t{}  TOC added.\t[{}]'.format(
                EMOJI_SUCESS, self.notebook_path), fg='green')

        with open(self.notebook_path, 'w') as file:
            file.write(json.dumps(ipynb, indent=2))

    def remove_toc(self, ipynb, position):
        del ipynb['cells'][position]

        with open(self.notebook_path, 'w') as file:
            file.write(json.dumps(ipynb, indent=2))

        click.secho('\t{}  TOC removed.\t[{}]'.format(
            EMOJI_SUCESS, self.notebook_path), fg='green')

    def compute_toc(self):
        try:
            ipynb = self.read_notebook_content()
            markdown_cells = self.get_markdown_cells(ipynb)
            update_toc, position = self.find_existing_toc(ipynb)

            # Check if there is an existing TOC
            if self.delete and isinstance(position, int):
                self.remove_toc(ipynb, position)
            elif self.delete:
                click.secho(
                    '\t{}  File has no TOC.\t[{}]'.format(
                        EMOJI_WARNING, self.notebook_path),
                    fg='yellow')
            else:
                markdown_lines = self.get_markdown_lines(markdown_cells)
                headers = self.get_headers(markdown_lines)
                toc = self.build_toc(headers)
                if not self.stdout:
                    self.write_toc(ipynb, toc, update_toc, position)
                else:
                    click.secho('\t{}  TOC built.\t[{}]'.format(
                        EMOJI_SUCESS, self.notebook_path), fg='green')
                    click.echo(''.join(toc))
        except Exception as err:
            click.secho(
                '\t{}  Build failed.\t[{}]'.format(
                    EMOJI_FAILURE, self.notebook_path),
                fg='red')
            raise(err)