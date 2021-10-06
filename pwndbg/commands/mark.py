#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import pwndbg.commands
import pwndbg.memview.memory

parser = argparse.ArgumentParser(description="""
    Mark specified address and displays its location on GUI
    (Usage: mark <address>)
    """)
parser.add_argument("address", nargs="?", default=None, type=int, help="The address to show in memview")
@pwndbg.commands.ArgparsedCommand(parser)
@pwndbg.commands.OnlyWhenRunning
def mark(address=None):
    """
    Mark specified address and displays its location on GUI
    """
    if address==None:
        return False

    meminfo = pwndbg.memview.memory.set("marks", int(address))
    return True
