# help.py

__version__ = '1.0.0' # Major.Minor.Patch

from sh import get_bins, cmds_integrated


def __main__(args):
    print ("Available commands:")
    for k in cmds_integrated:
        print ("{}".format(k))
    
    print ("")
    print ("Available bins:")
    pybins, shbins = get_bins()
    for k in pybins:
        print ("{}".format(k))
    for k in shbins:
        print ("{}".format(k))
    print ("")


