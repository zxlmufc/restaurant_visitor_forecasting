# -*- coding: utf-8 -*-
"""
@author: Xiaolan Zhu <xiaolan.zhu7@outlook.com>

"""

import pandas as pd
from pandas.tseries.offsets import Day
from preparation import utils


def calc_store_utlity_capacity(data, full_train=False):
    """
    :param data: air_visit data
    :param full_train: if full_train == True, rows in the validation set will be included in the calculation
    :return:
    """
    
    if not full_train:
        air_visit = data.loc[data.is_eval == "train"]
        
    store_utils = air_visit.groupby("air_store_id", group_keys=False).apply(lambda x: pd.Series({
        "first_appear": x.visit_date.dt.date.min(),
        "days_has_visit": x.shape[0],
        "capacity": x.visitors.max()
    }))
    store_utils["lasting_days"] = air_visit.visit_date.dt.date.max() - store_utils.first_appear + Day(1)
    store_utils["lasting_days"] = store_utils.lasting_days.dt.days
    store_utils['utility_rate'] = store_utils.days_has_visit / store_utils.lasting_days
    
    use_cols = ["lasting_days", "days_has_visit", "utility_rate", "capacity"]
    utils.save_pickle(store_utils[use_cols].add_prefix("store_"), "store_feature.p")


if __name__ == "__main__":
    air_visit = utils.load_pickle("air_visit.p")
    calc_store_utlity_capacity(air_visit, full_train=False)
