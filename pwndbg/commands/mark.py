#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints out pointer chains starting at some address in memory.

Generally used to print out the stack or register values.
"""

import argparse
import collections
import math

import pwndbg.arch
import pwndbg.chain
import pwndbg.color.telescope as T
import pwndbg.color.theme as theme
import pwndbg.commands
import pwndbg.config
import pwndbg.memory
import pwndbg.regs
import pwndbg.typeinfo
import pwndbg.memview.memory

# telescope_lines = pwndbg.config.Parameter('telescope-lines', 8, 'number of lines to printed by the telescope command')
# skip_repeating_values = pwndbg.config.Parameter('telescope-skip-repeating-val', True,
                                                # 'whether to skip repeating values of the telescope command')
# skip_repeating_values_minimum = pwndbg.config.Parameter('telescope-skip-repeating-val-minimum', 3,
                                                        # 'minimum amount of repeated values before skipping lines')

# offset_separator = theme.Parameter('telescope-offset-separator', '│', 'offset separator of the telescope command')
# offset_delimiter = theme.Parameter('telescope-offset-delimiter', ':', 'offset delimiter of the telescope command')
# repeating_marker = theme.Parameter('telescope-repeating-marker', '... ↓',
                                   # 'repeating values marker of the telescope command')


parser = argparse.ArgumentParser(description="""
    Mark specified address and displays its location on GUI
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

    meminfo = pwndbg.memview.memory.set("marks", address):
    return True
