#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch information on heap
"""

import pwndbg.heap
import pwndbg.symbol

class HeapInfo:
    """
    Like MemInfo, but about heaps
    [<start>, <end>]
    """

    main_arena = [-1, -1]
    top_chunk = [-1, -1]
    malloc_hook = [-1, -1]
    free_hook = [-1, -1]

def get(heap_start_end):
    """
    main wrapper function to call all other fetches

    Args:
        - heap_start_end (list): Start/end address of heap given by MemInfo class. If heap is uninitialized, value is [-1, -1]
    """

    heapinfo = HeapInfo()
    get_main_arena(heapinfo)
    get_top_chunk(heapinfo, heap_start_end[1])
    get_malloc_free_hook(heapinfo)

    if(heap_start_end[0]==-1):
        return "heap       uninitialized"
    else:
        heapstring = "\n".join([
            "heap        %s-%s" % (hex(heap_start_end[0]), hex(heap_start_end[1])),
            "main_arena  %s-%s" % (hex(heapinfo.main_arena[0]), hex(heapinfo.main_arena[1])),
            "top_chunk   %s-%s" % (hex(heapinfo.top_chunk[0]), hex(heapinfo.top_chunk[1])),
            "malloc_hook %s-%s" % (hex(heapinfo.malloc_hook[0]), hex(heapinfo.malloc_hook[1])),
            "free_hook   %s-%s" % (hex(heapinfo.free_hook[0]), hex(heapinfo.free_hook[1]))
            ])
        return heapstring

def get_main_arena(heapinfo):
    heap = pwndbg.heap.current
    heapinfo.main_arena[0] = pwndbg.symbol.address('main_arena')
    heapinfo.main_arena[1] = heap.main_arena["max_system_mem"].address + 8 # max_system_mem is the last entry of the main arena
    
def get_top_chunk(heapinfo, heap_end):
    allocator = pwndbg.heap.current
    heapinfo.top_chunk[0] = allocator.get_arena()["top"] 
    heapinfo.top_chunk[1] = heap_end

def get_malloc_free_hook(heapinfo):
    heapinfo.malloc_hook[0] = pwndbg.symbol.address('__malloc_hook')
    heapinfo.malloc_hook[1] = pwndbg.symbol.address('__malloc_hook') + 8 # malloc hook is a quadword
    heapinfo.free_hook[0] = pwndbg.symbol.address('__free_hook')
    heapinfo.free_hook[1] = pwndbg.symbol.address('__free_hook') + 8 # free hook is a quadword
