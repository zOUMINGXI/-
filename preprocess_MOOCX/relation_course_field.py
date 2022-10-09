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


# data dataframe格式
# left course实体link文件， right filed实体link文件
# 双向关系
def get_relation_course_field_KG(left_link_path, right_link_path, data):
    with open("relation_course_field.kg", "w", encoding="UTF-8") as file:
        file.write("head_id:token\trelation_id:token\ttail_id:token\n")
        for i in range(len(data["course_id"])):
            # 取100条
            if i >= 100:
                break
            for j in range(len(data["field"][i])):
                # 某课程与某领域相关
                file.write(get_entity_name(left_link_path, data["id"]))
                file.write("\t")
                # 关系id规则不太明确，如果出问题可以自行修改
                file.write("course.course.fields")
                file.write("\t")
                file.write(get_entity_name(right_link_path, data["field"][i][j]))
                file.write("\n")
                # 某领域包含某课程
                file.write(get_entity_name(right_link_path, data["field"][i][j]))
                file.write("\t")
                file.write("field.field.contain_courses")
                file.write("\t")
                file.write(get_entity_name(left_link_path, data["id"]))
                file.write("\n")


# def get_relation_course_field_link(data):
#     with open("get_relation_course_field.link", "w", encoding="UTF-8") as file:
#         file.write("item_id:token\tentity_id:token\n")
#         for i in range(len(data["course_id"])):
#             if i >= 100:
#                 break
#             file.write(data["course_id"])
#             file.write("\t")
#             file.write("courses." + data["id"][i])
#             file.write("\n")
