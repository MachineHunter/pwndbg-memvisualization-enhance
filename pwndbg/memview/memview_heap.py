#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch information on heap
"""

import pwndbg.heap

class HeapInfo:
    """
    Like MemInfo, but about heaps
    [<start>, <end>]
    """

    main_arena = [-1, -1]

def get(heap_info):
    """
    main wrapper function to call all other fetches

    Args:
        - heap_info (list): Start/end address of heap given by MemInfo class. If heap is uninitialized, value is [-1, -1]
    """

    heapinfo = HeapInfo()
    get_main_arena(heapinfo)

    if(heap_info[0]==-1):
        return "heap       uninitialized"
    else:
        heapstring = "\n".join([
            "heap       %s-%s" % (hex(heap_info[0]), hex(heap_info[1])),
            "main_arena %s-s" % (hex(heap_info[0])) 
            ])
        return heapstring

def get_main_arena(heapinfo):
    allocator = pwndbg.heap.current
    heapinfo.main_arena[0] = allocator.get_arena()["top"]
