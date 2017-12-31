# -*- coding: utf-8 -*-
"""
@author: Xiaolan Zhu <xiaolan.zhu7@outlook.com>

"""

import os
import re
from pprint import pprint
from zipfile import ZipFile

import time
import joblib
import pandas as pd
from preparation import config


def read_zip(zip_dir):
    with ZipFile(zip_dir) as myzip:
        file_name = re.sub("\.zip$", "", zip_dir.split("/")[-1])
        with myzip.open(file_name) as myfile:
            return pd.read_csv(myfile)


def save_pickle(df,name):
    cache_dir = config.cache_dir
    joblib.dump(df, os.path.join(cache_dir, name))
    print("Saving file object to: {}".format(os.path.abspath(os.path.join(cache_dir, name))))


def laod_pickle(file_name, default_dir=None):
    default_dir = config.cache_dir if \
        default_dir is None else default_dir
    out = joblib.load(os.path.join(default_dir, file_name))
    pprint(out.head(5))
    print("\n{} is of shape: {}".format(file_name, out.shape))
    return out


def start(fname):
    global st_time
    st_time = time.time()
    print("""
#==============================================================================
# START !!! {} PID: {}
#==============================================================================
""".format(fname, os.getpid()))
    
    return


def end(fname):
    print("""
#==============================================================================
# SUCCESS !!! {}
#==============================================================================
""".format(fname))
    print('time: {:.2f}min'.format((time.time() - st_time) / 60))
    return
