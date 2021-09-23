#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
memory information for memory visualization tool
"""
import pwndbg.vmmap


class MemInfo:
    """
    page = [<start>, <end>]
    """
    executable = [-1, -1]
    libc       = [-1, -1]
    ld         = [-1, -1]
    stack      = [-1, -1]


def get():
    meminfo = MemInfo()
    get_vmmap(meminfo)
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
                meminfo.executable[0] = page.start
                meminfo.executable[1] = page.end
        if page.is_stack:
            meminfo.stack[0] = page.start
            meminfo.stack[1] = page.end
    
    return meminfo
