#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch information on heap
"""

import pwndbg.heap
import pwndbg.symbol
import pwndbg.commands
import pwndbg.typeinfo

class HeapInfo:
    """
    Like MemInfo, but about heaps
    [<start>, <end>]
    """

    main_arena = [-1, -1]
    top_chunk = [-1, -1]
    malloc_hook = [-1, -1]
    free_hook = [-1, -1]
    chunks = [-1, -1]

def get(heap_start_end):
    """
    main wrapper function to call all other fetches

    Args:
        - heap_start_end (list): Start/end address of heap given by MemInfo class. If heap is uninitialized, value is [-1, -1]
    """

    heapinfo = HeapInfo()

    if(heap_start_end[0]==-1):
        return "heap       uninitialized"
    else:
        get_main_arena(heapinfo)
        get_top_chunk(heapinfo, heap_start_end[1])
        get_malloc_free_hook(heapinfo)
        get_main_chunks(heapinfo)
        heapstring = "\n".join([
            "heap        %s-%s" % (hex(heap_start_end[0]), hex(heap_start_end[1])),
            "main_arena  %s-%s" % (hex(heapinfo.main_arena[0]), hex(heapinfo.main_arena[1])),
            "top_chunk   %s-%s" % (hex(heapinfo.top_chunk[0]), hex(heapinfo.top_chunk[1])),
            "malloc_hook %s-%s" % (hex(heapinfo.malloc_hook[0]), hex(heapinfo.malloc_hook[1])),
            "free_hook   %s-%s" % (hex(heapinfo.free_hook[0]), hex(heapinfo.free_hook[1])),
            "chunks      %s" % ([hex(addr) for addr in heapinfo.chunks[0]])
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
    
def get_main_chunks(heapinfo):
    """
    Most of code ported directly from vis_heap_chunks() in pwndbg/commands/heap.py
    (TODO: Refactor for DRY/efficiency)
    """
    addr = None 
    count = None
    naive = None

    allocator = pwndbg.heap.current
    heap_region = allocator.get_heap_boundaries(addr)
    arena = allocator.get_arena_for_chunk(addr) if addr else allocator.get_arena()
    
    top_chunk = arena['top']
    ptr_size = allocator.size_sz

    # Build a list of addresses that delimit each chunk.
    chunk_delims = []
    if addr:
        cursor = int(addr)
    elif arena == allocator.main_arena:
        cursor = heap_region.start
    else:
        cursor = heap_region.start + allocator.heap_info.sizeof
        if pwndbg.vmmap.find(allocator.get_heap(heap_region.start)['ar_ptr']) == heap_region:
            # Round up to a 2-machine-word alignment after an arena to
            # compensate for the presence of the have_fastchunks variable
            # in GLIBC versions >= 2.27.
            cursor += (allocator.malloc_state.sizeof + ptr_size) & ~allocator.malloc_align_mask
        
    # Check if there is an alignment at the start of the heap, adjust if necessary.
    if not addr:
        first_chunk_size = pwndbg.arch.unpack(pwndbg.memory.read(cursor + ptr_size, ptr_size))
        if first_chunk_size == 0:
             cursor += ptr_size * 2
        
    cursor_backup = cursor

    while(1):
        # Don't read beyond the heap mapping if --naive or corrupted heap.
        if cursor not in heap_region:
            chunk_delims.append(heap_region.end)
            break

        size_field = pwndbg.memory.u(cursor + ptr_size)
        real_size = size_field & ~allocator.malloc_align_mask
        prev_inuse = allocator.chunk_flags(size_field)[0]

        # Don't repeatedly operate on the same address (e.g. chunk size of 0).
        if cursor in chunk_delims or cursor + ptr_size in chunk_delims:
            break

        if prev_inuse:
            chunk_delims.append(cursor + ptr_size)
        else:
            chunk_delims.append(cursor)

        if (cursor == top_chunk and not naive) or (cursor == heap_region.end - ptr_size*2):
            chunk_delims.append(cursor + ptr_size*2)
            break

        cursor += real_size

    heapinfo.chunks[0] = chunk_delims
