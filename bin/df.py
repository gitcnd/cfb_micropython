# df.py

__version__ = '1.0.0' # Major.Minor.Patch

from sh import human
import os


def __main__(args):
    _print_mount_stats("/")

    for pt in os.ilistdir("/"):
        f = pt[0]
        if len(pt) == 3:#Currently means vfs mount point
            print ("")
            _print_mount_stats("/"+f)

def _print_mount_stats(path):
    info = os.statvfs(path)
    block_size = info[0]
    fragment_size = info[1]
    fragment_count = info[2]
    free_block_count = info[3]

    print ("Filesystem '{}'\t{}-blocks\t\ttotal {}\tfree {}".format(path, block_size, fragment_count, free_block_count))
    used = (fragment_count - free_block_count) * block_size
    free = free_block_count * block_size
    print ("\t\tUSED {} bytes\t{}".format(used, human(used)))
    print ("\t\tFREE {} bytes\t{}".format(free, human(free)))


