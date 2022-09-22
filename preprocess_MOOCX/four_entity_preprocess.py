import json
import os
import numpy as np
import pandas as pd
import time
import re
import sys
import codecs
import pickle

from pyasn1.compat.octets import null

from data_generation_Cube import read_wrong_json


def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df

def get_user_id_name_courseid_index():#提取用户id，name并创建索引
    data=read_json("../scripts/entities/user.json")
    data=data[["id","name"]]
    data = data.reset_index()
    # print(data)
    return data
# get_user_id_name_courseid_index()
def get_concept_id_name_index():#提取概念id，name并创建索引
    data=read_json("../scripts/entities/concept.json")
    data=data[["id","name"]]
    data=data.reset_index()
    return data
    # print(data)
# get_concept_id_name_index()
def get_course_id_name_index():#提取课程id name，field并创建索引
    data=read_json("../scripts/entities/course.json")
    data=data[["id","name","field"]]
    data=data.reset_index()
    return data
    # print(data["field"].value_counts())
    # return data
# get_course_id_name_index()
def get_video_id_ccid_index():
    data=pd.read_csv("../scripts/relations/video_id-ccid.txt", sep='\t', header=None)
    data.columns=['id','ccid']
    data['index']=range(len(data))
    print(data)
# get_video_id_ccid_index()














