import json
import numpy as np
import pandas as pd
import time
import re
import sys
import codecs
import pickle
import four_entity_preprocess


def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df


def get_user_course_relation():  # index:id:course_order
    data = read_json("../scripts/entities/user.json")
    data = data[["id", "course_order"]].reset_index()
    return data
# get_user_course_relation()


# 此函数生成csv文件
def get_user_course_relation_csv(data):
    data.to_csv("get_user_course_relation.csv", mode="w", index=False)


# 此函数生成pickle文件
def get_user_course_relation_pickle(data):
    data.to_pickle("get_user_course_relation.pkl")


# get_user_course_relation_csv(get_user_course_relation())
