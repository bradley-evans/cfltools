"""
CLI interface tests
"""
import pytest
import click
from click.testing import CliRunner
from .objects import CLISession


def test_about():
    from cfltools.cli import about
    runner = CliRunner()
    result = runner.invoke(about)
    assert result.exit_code == 0

def test_clisession(testdb, logfile):
    session = CLISession(testdb)
    session.logparse(logfile)
    