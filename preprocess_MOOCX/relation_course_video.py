import json
import numpy as np
import pandas as pd
import time
import re
import sys
import codecs
import pickle


def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df


# def read_wrong_json(file):
#     with open(file, "r", encoding='utf-8') as f:
#         data = f.readlines()
#         df = pd.DataFrame([re.split('\t|\n', x) for x in data])
#         df = df.drop([2], axis=1)
#     return df

def get_relation_course_video():
    data = read_json("../scripts/entities/course.json")
    data_resource = data[["resource"]]
    df = dict()
    for i in range(0, len(data_resource)):
        data_id = data["id"].iloc[i]
        df[str(data_id)] = [[]]
        for j in range(0, len(data_resource.iloc[i])):
            ar = data_resource.iloc[i]
            dic = ar[j]
            for h in range(0, len(dic)):
                str1 = dic[h]
                df[str(data_id)][0].append(str(str1["resource_id"]))

    # df字典key是course_id , value是video_id 的列表
    df_result = pd.DataFrame.from_dict(df, orient="index", columns=['video_id'])
    df_result = df_result.reset_index()
    df_result = df_result.rename(columns={'index': 'course_id'})
    return df_result


def get_relation_course_video_csv(df_result):
    df_result.to_csv("get_relation_course_video.csv", mode="w", index=False)


# 此函数生成pickle文件
def get_relation_course_video_pickle(data):
    data.to_pickle("get_relation_course_video.pkl")


# get_relation_course_video_csv(get_relation_course_video())


def get_relation_course_video_KG(data):
    with open("get_relation_course_video.kg", "w", encoding="UTF-8") as file:
        file.write("head_id:token\trelation_id:token\ttail_id:token\n")
        for i in range(len(data["course_id"])):
            if i >= 100:
                break
            for j in range(len(data["video_id"][i])):
                file.write("courses." + data["id"])
                file.write("\t")
                file.write("courses.course.contain")
                file.write("\t")
                file.write(data["video_id"][i][j])
                file.write("\n")


def get_relation_course_video_link(data):
    with open("get_relation_course_video.link", "w", encoding="UTF-8") as file:
        file.write("item_id:token\tentity_id:token\n")
        for i in range(len(data["course_id"])):
            if i >= 100:
                break
            file.write(data["course_id"])
            file.write("\t")
            file.write("courses." + data["id"][i])
            file.write("\n")

