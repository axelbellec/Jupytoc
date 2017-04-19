from click.testing import CliRunner

from jupytoc import cli
from jupytoc.constants import EMOJI_WARNING, EMOJI_FAILURE, EMOJI_JUPYTOC


def test_toc_builder_empty_files():
    runner = CliRunner()
    with runner.isolated_filesystem():
        for i in range(2):
            with open('notebook_test_{}.ipynb'.format(i), 'w') as f:
                f.write('')

        notebooks = ['notebook_test_{}.ipynb'.format(i) for i in range(2)]
        result = runner.invoke(cli, notebooks)
        assert result.output == '{emoji_jupitoc}  Jupytoc is building TOC for {nb} notebook(s)\n\t{emoji_warn}  Empty file.\t[notebook_test_0.ipynb]\n\t{emoji_warn}  Empty file.\t[notebook_test_1.ipynb]\nDone.\n'.format(
            nb=len(notebooks), emoji_jupitoc=EMOJI_JUPYTOC, emoji_warn=EMOJI_WARNING)


def test_no_input_file():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.output == '\t{}  You must pass at least 1 notebook.\n'.format(EMOJI_FAILURE)
