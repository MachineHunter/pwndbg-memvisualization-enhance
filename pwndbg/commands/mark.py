#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import pwndbg.commands
import pwndbg.perceptor.memory


# mark
parser = argparse.ArgumentParser(description="""
    Mark specified address and displays its location on GUI
    (Usage: mark <address>)
    """)
parser.add_argument("address", nargs="?", default=None, type=int, help="The address to show in perceptor")
@pwndbg.commands.ArgparsedCommand(parser)
@pwndbg.commands.OnlyWhenRunning
def mark(address=None):
    """
    Mark specified address and displays its location on GUI
    """
    if address==None:
        return False

    meminfo = pwndbg.perceptor.memory.set("marks", int(address))
    return True


# unmark
parser = argparse.ArgumentParser(description="""
    Unmark meminfo.marks of specified index
    (Usage: unmark <index>)
    """)
parser.add_argument("index", nargs="?", default=None, type=int, help="The index of mark to remove")
@pwndbg.commands.ArgparsedCommand(parser)
@pwndbg.commands.OnlyWhenRunning
def unmark(index=None):
    """
    Unark specified index stored in meminfo.marks
    """
    if index==None:
        return False

    meminfo = pwndbg.perceptor.memory.unset("marks", int(index))
    return True
