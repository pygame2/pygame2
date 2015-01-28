#!c:\windows\system32\cmd.exe /c python.exe

import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this)); del os, activate_this

# EASY-INSTALL-ENTRY-SCRIPT: 'Pygments==1.6','console_scripts','pygmentize'
__requires__ = 'Pygments==1.6'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Pygments==1.6', 'console_scripts', 'pygmentize')()
    )