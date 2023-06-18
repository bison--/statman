from conf import *

try:
    from conf_local import *
except ModuleNotFoundError:
    # print('WARNING: conf_local.py does not exist.')
    pass
