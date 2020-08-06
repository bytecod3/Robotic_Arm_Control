# check if required modules exist and if not install them
import sys
import subprocess
import pkg_resources

required = {'tk_tools','pyserial','pyfirmata','python3-tk','pmw'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python3 = sys.executable()
    subprocess.check_call([python3, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
