import json

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


# def get_course_id_field_res_id():
#     writer = open('数据第一次处理仅提取/course_field_resource.txt', 'w', encoding='utf-8')
#     df = read_json("./scripts/entities/course.json")
#     df_head = df.head()
#     for df_id, df_field in (df_head["id"], df_head["field"]):
#         writer.write(df_id + " " + df_field)
#     writer.close()


# get_course_id_field_res_id()

# def get_course_id_name_index():
#     writer = open('数据第一次处理仅提取/course_id__name_index.txt', 'w', encoding='utf-8')
#     data = read_json("./scripts/entities/course.json")
#     # data = pd.DataFrame(data, columns=['id', 'name'])
#     data = data[["id", "name"]]
#     print(data)

# get_course_id_name_index()
    # writer.close()
    # data.to_json("数据第一次处理仅提取/course_id_index.json")
# user_id_index=dict()
# course_id_index=dict()
# get_course_id_index()


# def get_course_id_index():#创建索引字典
#     data=read_json("./scripts/entities/course.json")
#     # writer = open('数据第一次处理仅提取/course_id_index.json', 'w', encoding='utf-8')
#     i=0
#     for course_id in data["id"]:
#         # writer.write(course_id+" "+str(i)+"\n")
#         course_id_index[course_id]=i
#         i+=1
#     # writer.close()
# # get_course_id_index()
def get_user_id_name_courseid_index():#提取用户id，name并创建索引
    data=read_json("../scripts/entities/user.json")
    data=data[["id","name"]]
    data = data.reset_index()
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
    data=read_json("./scripts/entities/course.json")
    data=data[["id","name","field"]]
    data=data.reset_index()
    return data
    # print(data["field"].value_counts())
    # return data
# get_course_id_name_index()
















