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


# 从link文件中获取对应的实体名
# link_path link文件路径, item_id 搜寻的实体id
def get_entity_name(link_path, item_id):
    with open(link_path, "r", encoding="UTF-8") as link_file:
        i = 0
        while True:
            data = link_file.readline()
            if not data:
                return None
            else:
                if i == 0:
                    i += 1
                else:
                    data = data.split("\t")
                    if data[0] == item_id:
                        return data[1]
                    else:
                        i += 1


# left user实体link文件， right course实体link文件
def get_user_course_relation_KG(left_link_path, right_link_path, data):
    with open("user_course_relation.kg", "w", encoding="UTF-8") as file:
        file.write("head_id:token\trelation_id:token\ttail_id:token\n")
        for i in range(len(data["id"])):
            if i >= 100:
                break
            for j in range(len(data["course_order"][i])):
                # 某用户选择了某课程
                file.write(get_entity_name(left_link_path, data["id"]))
                file.write("\t")
                # 关系id规则不太明确，如果出问题可以自行修改
                file.write("user.user.take_courses")
                file.write("\t")
                file.write(get_entity_name(right_link_path, data["course_order"][i][j]))
                file.write("\n")
                # 某课程被某用户选择
                file.write(get_entity_name(right_link_path, data["course_order"][i][j]))
                file.write("\t")
                file.write("course.course.taken_by")
                file.write("\t")
                file.write(get_entity_name(left_link_path, data["id"]))
                file.write("\n")


# def get_user_course_relation_link(data):
#     with open("get_user_course_relation.link", "w", encoding="UTF-8") as file:
#         file.write("item_id:token\tentity_id:token\n")
#         for i in range(len(data["id"])):
#             if i >= 100:
#                 break
#             file.write(data["id"])
#             file.write("\t")
#             file.write("users." + data["id"][i])
#             file.write("\n")
