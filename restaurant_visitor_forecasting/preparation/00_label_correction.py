# -*- coding: utf-8 -*-
"""
@author: Xiaolan Zhu <xiaolan.zhu7@outlook.com>

"""
from datetime import datetime

import pandas as pd

from preparation import utils

utils.start(__file__)


# ===============================================================================
# Reservation info by platform
# ===============================================================================

air_reserve = utils.read_zip('../resources/raw/air_reserve.csv.zip')
air_reserve['visit_datetime'] = pd.to_datetime(air_reserve['visit_datetime'], format="%Y-%m-%d %H:%M:%S")
air_reserve['reserve_datetime'] = pd.to_datetime(air_reserve['reserve_datetime'], format="%Y-%m-%d %H:%M:%S")
air_reserve['in_advance'] = air_reserve['visit_datetime'] - air_reserve['reserve_datetime']

utils.save_pickle(air_reserve,"air_reserve.p")

hpg_reserve = utils.read_zip('../resources/raw/hpg_reserve.csv.zip')
hpg_reserve['visit_datetime'] = pd.to_datetime(hpg_reserve['visit_datetime'], format="%Y-%m-%d %H:%M:%S")
hpg_reserve['reserve_datetime'] = pd.to_datetime(hpg_reserve['reserve_datetime'], format="%Y-%m-%d %H:%M:%S")
hpg_reserve['in_advance'] = hpg_reserve['visit_datetime'] - hpg_reserve['reserve_datetime']

utils.save_pickle(hpg_reserve,"hpg_reserve.p")

# ===============================================================================
# store info by platform
# ===============================================================================

air_store = utils.read_zip('../resources/raw/air_store_info.csv.zip')
utils.save_pickle(air_store,"air_store.p")

hpg_store = utils.read_zip('../resources/raw/hpg_store_info.csv.zip')
utils.save_pickle(hpg_store,"hpg_store.p")

store_id_relation = utils.read_zip('../resources/raw/store_id_relation.csv.zip')
utils.save_pickle(store_id_relation,"store_id_relation.p")

# ===============================================================================
# date info
# ===============================================================================
date_info = utils.read_zip('../resources/raw/date_info.csv.zip')
date_info['calendar_date'] = pd.to_datetime(date_info.calendar_date, format="%Y-%m-%d")
date_info['calendar_year'] = date_info['calendar_date'].dt.year
date_info['calendar_month'] = date_info['calendar_date'].dt.month
date_info['calendar_day'] = date_info['calendar_date'].dt.day
date_info['calendar_dow'] = date_info['calendar_date'].dt.dayofweek

quarter_map = dict(zip([i for i in range(12)], [int(i/3) for i in range(0, 12)]))  # quarter by temperature
date_info["calendar_quarter"] = date_info.calendar_month.map(quarter_map)
utils.save_pickle(date_info, "date_info.p")

# ===============================================================================
# test data
# ===============================================================================

test_visit = utils.read_zip('../resources/raw/sample_submission.csv.zip')

test_visit["visit_date"] = test_visit["id"].map(lambda x: x.split("_")[-1])
test_visit['air_store_id'] = test_visit["id"].map(lambda x: "_".join(x.split("_")[:-1]))
test_visit["visit_date"] = pd.to_datetime(test_visit["visit_date"], format="%Y-%m-%d")
test_visit["visitors"] = -1
test_visit['is_eval'] = "test"

# This is for produce submission
utils.save_pickle(test_visit[['id','visit_date','air_store_id']], "test_id.p")

# ===============================================================================
# train data
# ===============================================================================

air_visit = utils.read_zip('../resources/raw/air_visit_data.csv.zip')
air_visit.sort_values(by=["air_store_id", "visit_date"], inplace=True)
air_visit['visit_date'] = pd.to_datetime(air_visit['visit_date'], format="%Y-%m-%d")

# ===============================================================================
# correct typo in number of visits, see notebook for details
# air_store_id, visit_date, visitors
# ===============================================================================

correction = [("air_8c3175aa5e4fc569", "2017-04-18", 177),
              ("air_51281cd059d7b89b", "2017-03-21", 26),
              ("air_81bd68142db76f58", "2017-03-28", 35)]

for rid, d, n in correction:
    air_visit.loc[(air_visit["air_store_id"] == rid) & (air_visit["visit_date"] == d), "visitors"] = n

# ===============================================================================
# train test split:
# train: data prior to 2017-03-14 (excluding 03-14)
# eval: data between 2017-03-14 - 2017-04-22 (39 days)
# test: data between 2017-04-23 - 2017-05-31 (39 days)
# ===============================================================================
eval_start_day = datetime.strptime("2017-03-14", "%Y-%m-%d")
air_visit['is_eval'] = "train"
air_visit.loc[air_visit['visit_date'] >= eval_start_day, "is_eval"] = "eval"

utils.save_pickle(air_visit, "air_visit.p")

usecols = ['air_store_id', "visit_date", "is_eval", "visitors"]
lable = pd.concat([air_visit.loc[:, usecols], test_visit.loc[:, usecols]], ignore_index=True)

utils.save_pickle(air_visit, "lable.p")

utils.end(__file__)
