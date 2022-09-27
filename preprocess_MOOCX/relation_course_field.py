import pandas as pd
import json


def get_relation_course_field():
    data = pd.read_json("course-field.json", lines=True)
    return data


def get_relation_course_field_csv(data):
    data.to_csv("get_relation_course_field.csv", mode="w", index=False)


# 此函数生成pickle文件
def get_relation_course_field_pickle(data):
    data.to_pickle("get_relation_course_field.pkl")


# get_relation_course_field_csv(get_relation_course_field())
