# init.py

__version__ = '1.0.0' # Major.Minor.Patch

import config
print("\033]0;{}\007http://{}.local/".format(config.HOSTNAME,config.HOSTNAME))  # \033]0; sets terminal window title
