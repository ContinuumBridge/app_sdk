#!/usr/bin/env python
import os
import sys
import contextlib

if __name__ == "__main__":

    os.environ.setdefault("CB_PROJECT_ROOT", os.path.abspath(os.path.dirname(__file__)))

    from cb.management import cli

    cli()

