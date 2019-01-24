#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import contextlib


@contextlib.contextmanager
def remember_cwd():
    curdir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(curdir)


def ensure_dir(file_path):
    """ensure the dir exist. Check the dir, if not exist create one"""
    directory = os.path.dirname(file_path)
    if directory == "":
        directory = "./"
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_size(start_path='.'):
    """
    Return the total size of the path.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    # logging.debug("Got size for {0}: {1}".format(start_path, total_size))
    return total_size


def smartCopy(src, des):
    """Copy srcFile to des directory.
    If the filename already been used, add a 0 at the end of the filename.

    :src: The src file. Must exists.
    :des: The des directory. Must be a directory and exist.
          If not end with '/', '/' will be added automatically.

    """
    if not des.endswith("/"):
        des += "/"
    filename = os.path.basename(src)
    rawname, ext = os.path.splitext(filename)
    if not os.path.exists(os.path.join(des, filename)):
        shutil.copy(src, des)
        return
    seq = 0
    newfilePath = os.path.join(des, "{0}{1}{2}".format(rawname, seq, ext))
    while os.path.exists(newfilePath):
        seq += 1
        newfilePath = os.path.join(des, "{0}{1}{2}".format(rawname, seq, ext))
    shutil.copy(src, newfilePath)

if __name__ == '__main__':
    pass
    ensure_dir("./Config/")
