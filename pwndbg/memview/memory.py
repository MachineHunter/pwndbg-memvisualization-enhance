#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
memory information for memory visualization tool
"""
from elftools.elf.elffile import ELFFile
import pwndbg.vmmap


class MemInfo:
    """
    page = [<start>, <end>]
    """
    executable      = [-1, -1]
    text_section    = [-1, -1]
    plt_section     = [-1, -1]
    got_section     = [-1, -1]
    pltgot_section  = [-1, -1]
    gotplt_section  = [-1, -1]
    data_section    = [-1, -1]
    bss_section     = [-1, -1]
    libc            = [-1, -1]
    ld              = [-1, -1]
    stack           = [-1, -1]
    heap            = [-1, -1]

def get():
    meminfo = MemInfo()
    get_vmmap(meminfo)
    get_elfheader(meminfo)
    return meminfo

"""
can retrive
- executable mapped location
- stack location
- (?) heap location
- libc location
- loader location
"""
def get_vmmap(meminfo):
    vmmap = pwndbg.vmmap.get()

    for page in vmmap:
        if page.is_memory_mapped_file:
            filename = page.objfile.split("/")[-1]
            if filename[-3:]==".so":
                if filename[0:4]=="libc":
                    if meminfo.libc[0] == -1:
                        meminfo.libc[0] = page.start
                    if meminfo.libc[1] < page.end:
                        meminfo.libc[1] = page.end
                if filename[0:2]=="ld":
                    if meminfo.ld[0] == -1:
                        meminfo.ld[0] = page.start
                    if meminfo.ld[1] < page.end:
                        meminfo.ld[1] = page.end
            else:
                if meminfo.executable[0] == -1:
                    meminfo.executable[0] = page.start
                if meminfo.executable[1] < page.end:
                    meminfo.executable[1] = page.end
        if page.is_stack:
            meminfo.stack[0] = page.start
            meminfo.stack[1] = page.end
            
        if page.objfile=="[heap]":
            meminfo.heap[0] = page.start
            meminfo.heap[1] = page.end

    return meminfo


"""
can retrive
- section of loaded executable
"""
def get_elfheader(meminfo):
    local_path = pwndbg.file.get_file(pwndbg.proc.exe)

    with open(local_path, 'rb') as f:
        elffile = ELFFile(f)
        sections = []
        for section in elffile.iter_sections():
            start = section['sh_addr']

            # Don't print sections that aren't mapped into memory
            if start == 0:
                continue

            size = section['sh_size']
            sections.append((start, start + size, section.name))

        sections.sort()

        for start, end, name in sections:
            start += meminfo.executable[0]
            end   += meminfo.executable[0]
            if name == ".text":
                meminfo.text_section[0] = start
                meminfo.text_section[1] = end
            if name == ".data":
                meminfo.data_section[0] = start
                meminfo.data_section[1] = end
            if name == ".plt":
                meminfo.plt_section[0] = start
                meminfo.plt_section[1] = end
            if name == ".got":
                meminfo.got_section[0] = start
                meminfo.got_section[1] = end
            if name == ".plt.got":
                meminfo.pltgot_section[0] = start
                meminfo.pltgot_section[1] = end
            if name == ".got.plt":
                meminfo.gotplt_section[0] = start
                meminfo.gotplt_section[1] = end
            if name == ".bss":
                meminfo.bss_section[0] = start
                meminfo.bss_section[1] = end

