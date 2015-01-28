#!c:\windows\system32\cmd.exe /c python.exe

import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this)); del os, activate_this

# EASY-INSTALL-ENTRY-SCRIPT: 'nose==1.3.4','console_scripts','nosetests'
__requires__ = 'nose==1.3.4'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('nose==1.3.4', 'console_scripts', 'nosetests')()
    )