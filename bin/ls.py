# ls.py

__version__ = '1.1.0' # Major.Minor.Patch

from sh import human
import os


def __main__(args):
    ls(args[2:])    # mipyshell first 2 arguments are "python" and "photo.py"
def ls(args):
    path = ""
    if len(args) > 0:
        path = args[0]

    if len(path) == 0:
        path = os.getcwd()

    try:
        fstat=os.stat(path)
        if fstat[0] == 0x4000: # Check for directory bit

            print ("d .")
            if path != "/":
                print ("d ..")
                if path.endswith("/"):
                    path = path[:-1]

            path_pre = path + "/" if len(path) > 0 and path.endswith("/") == False else ""

            items = [pt for pt in os.ilistdir(path)]

            listems(items)
        else:
            listems([[path,fstat[0],fstat[1],fstat[6]]])
    except OSError:
        print("Not found") # Handle non-existent paths

def listems(items):
    for pt in sorted(items):
        #print(pt)    # ('notify.py', 32768, 0, 4604)A	# ('sd', 16384, 0)
        # >>> os.stat('sd/HoleTest2_0.2mm_PLA_MINI_19m.gcode')
        # (32768, 0, 0, 0, 0, 0, 1704870, 730410112, 730410112, 730410112)
        # >>> os.statvfs('sd/HoleTest2_0.2mm_PLA_MINI_19m.gcode')
        # (4096, 4096, 1895168, 1835183, 1835183, 0, 0, 0, 0, 255)
        # >>> os.stat('if.up')
        # (32768, 0, 0, 0, 0, 0, 13, 632, 632, 632)
        # >>> os.statvfs('if.up')
        # (4096, 4096, 512, 337, 337, 0, 0, 0, 0, 255)
        f = pt[0]
        type = pt[1]
        inode = pt[2]
        #fsize = None
        fsize = 0
        if len(pt) > 3:
            fsize = pt[3]
        if len(pt) > 4:
            fsize = pt[4]

        tag = "" if type == 32768 else "/"
        print ("{}\t{}{}".format(fsize, f,tag))
        #print ("{}\t{}{}".format(pt[3], f,tag))

        if 0:

            type = "f" if type == 32768 else "d"
            if fsize is None:
                type = "M"
            size = 0
            if type == "f":
                #print ("opening {}".format(path_pre + f))
                o = open(path_pre + f, "rb")
                size = human(o.seek(10000000))
                o.close()
            print ("{} {}    {}".format(type, size, f))



# When used outside of mipyshell...
if 'ARGV' in locals():
    ls(ARGV)    # invoked via REPL >>>    ARGV=["bin/"];exec(open("bin/ls.py").read())
else:
    pass # ls([])        # invoked via:        ampy --port $PORT run bin/photo.py
