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


def get_relation_course_field_KG(data):
    with open("get_relation_course_field.kg", "w", encoding="UTF-8") as file:
        file.write("head_id:token\trelation_id:token\ttail_id:token\n")
        for i in range(len(data["course_id"])):
            if i >= 100:
                break
            for j in range(len(data["field"][i])):
                file.write("courses." + data["id"])
                file.write("\t")
                file.write("courses.course.field")
                file.write("\t")
                file.write(data["field"][i][j])
                file.write("\n")


def get_relation_course_field_link(data):
    with open("get_relation_course_field.link", "w", encoding="UTF-8") as file:
        file.write("item_id:token\tentity_id:token\n")
        for i in range(len(data["course_id"])):
            if i >= 100:
                break
            file.write(data["course_id"])
            file.write("\t")
            file.write("courses." + data["id"][i])
            file.write("\n")
