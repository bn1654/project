from datetime import datetime
from os.path import splitext

def get_timstamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])