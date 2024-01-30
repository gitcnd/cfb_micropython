# git.py - extrmeely basic utility to emulate the "git pull" or "git clone" command on micropython

'''

Notes:-

1. Get the "git url" name

2. get the branch name, either from the .git/HEAD file or:-
perl -MJSON -e '$j=decode_json(`curl -s https://api.github.com/repos/gitcnd/mipyshell`);print $j->{default_branch}'

3. use gin utility to read all the file names out of .git/index - /home/cnd/Downloads/gin/gin index -j | prettyj  | grep -a "'name'"
or: recurse through curl -i GET https://api.github.com/repos/gitcnd/mipyshell/contents/

4. construct the URL to look like: https://raw.githubusercontent.com/gitcnd/mipyshell/master/LICENSE.md

'''


# Ways to run this program:-

# 1. With ampy
#       ampy --port $PORT run bin/photo.py
# example output:-
#       photo fn=out.jpg size=22((default)) quality=10
#       Length of buf: 23579

# 2. From REPL shell
#       >>> ARGV=["pic.jpg","5","10"];exec(open("bin/photo.py").read())
# example output:-
#       photo fn=pic.jpg size=5(FRAME_QVGA) quality=10
#       Length of buf: 9495

# 3. using mipyshell
# To run this program with arguments, install https://github.com/vsolina/mipyshell
# and save this file as bin/photo.py - then (for size 5 and quality 10):-
#       photo outfile.jpg 5 10

__version__ = '1.0.0' # Major.Minor.Patch  **CAUTION**  You must ALWAYS update this, so our self-updater works (littfs has no dates)

import requests

def __main__(args):
    run(args[2:])  # mipyshell first 2 arguments are "python" and "photo.py"

def run(args):
    if len(args) < 1:
        print("usage:\tARGV=['https://example.com/url_to_get.htm','outfile.htm'];exec(open('bin/wget.py').read())\t# -or-\n\twget https://example.com/url_to_get.htm [output filename]\n\t(use - for output filename to show on-screen")
    else:
        url = args[0]
        if len(args) > 1:
            filename = args[1]
        else:
            filename = ""
            if url.endswith("/"):
                filename = "index"
            else:
                filename = url.split("/")[-1].split("?")[0]
        try:
            r = requests.get(url).raw
            if filename != '-':
                fp = open(filename, "wt")
                print("\t {} => {} ".format(url,filename), end='\r')
        except Exception as e:
            print(f"Error '{e}' reading URL {url}")
            r = None
        if r:
            l = 0
            while (True):
                read = r.read(4096)
                l = l + len(read)
                if filename != '-':
                    fp.write(read)
                    print(" {} ".format(l), end='\r')
                else:
                    print(read.decode('unicode-escape') ,end='')
                if len(read) < 4096:
                    break

            if filename != '-':
                fp.close()
                print("")


if 'ARGV' in locals():
    run(ARGV)
