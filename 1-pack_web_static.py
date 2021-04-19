#!/usr/bin/python3
"""This fabric file compress the directory to be sent"""

from fabric.api import env, local, run
from datetime import datetime
import os

env.hosts = '35.196.27.222'
env.user = 'ubuntu'


def do_pack():
    """Sets the folder structure up and compresses directory"""

    check = local('mkdir -p versions')
    if (check.failed):
        return None
    now = datetime.now()
    file_name = "versions/web_static_" + \
                "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(now.year,
                                                          now.month,
                                                          now.day,
                                                          now.hour,
                                                          now.minute,
                                                          now.second) + \
                ".tgz"
    check = local('tar -zcvf {} ./web_static'.format(file_name))
    size_of = os.stat(file_name)
    if (check.failed):
        return None
    else:
        print("web_static packed: {} -> {}Bytes".format(file_name, size_of.st_size))
    return("versions/{}".format(file_name))
