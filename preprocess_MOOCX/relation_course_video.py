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
    data = read_json("../../原始数据/课程信息/course.json")
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
        # print(str(data_id))
        # print(df[str(data_id)])
    # df字典key是course id value是video_id 的列表
    df_result = pd.DataFrame.from_dict(df, orient="index")
    # df_result=df_result.reset_index()
    # df_result=df_result.rename(columns={'index':'course_id'})
    return df_result


def get_relation_course_video_csv(df_result):
    df_result.to_csv("get_relation_course_video.csv", mode="w", index=False)


get_relation_course_video_csv(get_relation_course_video())