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
def get_user_course_relation():#index:id:course_order
    data=read_json("../scripts/entities/user.json")
    data=data[["id","course_order"]].reset_index()
    return data
# get_user_course_relation()











