import os, sys
import contextlib
import click
import code
from .cb import CB
from .repl import PipedREPL
from .settings import PROJECT_ROOT

@click.group()
@contextlib.contextmanager
def cli():
    #print "manage cwd", os.path.dirname(os.path.realpath(__file__))
    #print "PROJECT_ROOT", PROJECT_ROOT
    print "sys.argv", sys.argv
    print "print in cli"
    click.echo('in cli')
    #click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
def run():
    cb = CB()
    cb.run()

@cli.command()
def shell():
    dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(dir, '__main__.py')
    repl = PipedREPL(bootstrap=file_path)
    repl.setup_cb()
    repl.start()

if __name__ == '__main__':
    cli()