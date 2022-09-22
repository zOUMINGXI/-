import pandas as pd
import json


# course.json比较小，可以直接返回dataFrame
def course_id_name_field_index(filename):
    data = pd.read_json("course.json", lines=True)
    with open(filename, "w", encoding="UTF-8") as file:
        for i in range(len(data)):
            new_data = {"id": data["id"][i], "name": data["name"][i], "field": data["field"][i], "index": i}
            json.dump(new_data, file, separators=(", ", ":"), ensure_ascii=False)
            file.write(",\n")


def course_id_name_field_index_df():
    data = pd.read_json("course.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"id": data["id"][i], "name": data["name"][i], "field": data["field"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


# video.json比较小，可以直接返回dataFrame
def video_ccid_name_text_index(filename):
    data = pd.read_json("video.json", lines=True)
    with open(filename, "w", encoding="UTF-8") as file:
        for i in range(len(data)):
            new_data = {"ccid": data["ccid"][i], "name": data["name"][i], "text": data["text"][i], "index": i}
            json.dump(new_data, file, separators=(", ", ":"), ensure_ascii=False)
            file.write(",\n")


def video_ccid_name_text_index_df():
    data = pd.read_json("video.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"ccid": data["ccid"][i], "name": data["name"][i], "text": data["text"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


# 下函数将处理后的data直接写入到文件中
def problem_pid_title_content_option_index(filename):
    data = pd.read_json("problem.json", lines=True)
    with open(filename, "w", encoding="UTF-8") as file:
        for i in range(len(data)):
            new_data = {"problem_id": data["problem_id"][i], "title": data["title"][i], "content": data["content"][i], "option": data["option"][i], "index": i}
            json.dump(new_data, file, separators=(", ", ":"), ensure_ascii=False)
            file.write(",\n")


# 下函数返回problem.json的dataFrame，但是文件太大，电脑内存不足
def problem_pid_title_content_option_index_df():
    data = pd.read_json("problem.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"problem_id": data["problem_id"][i], "title": data["title"][i], "content": data["content"][i], "option": data["option"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def school_id_name_index(filename):
    data = pd.read_json("school.json", lines=True)
    with open(filename, "w", encoding="UTF-8") as file:
        for i in range(len(data)):
            new_data = {"id": data["id"][i], "name": data["name"][i], "index": i}
            json.dump(new_data, file, separators=(", ", ":"), ensure_ascii=False)
            file.write(",\n")


# school.json数据量比较大，建议将数据写入文件中，而非返回dataFrame
def school_id_name_index_df():
    data = pd.read_json("school.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"id": data["id"][i], "name": data["name"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def teacher_id_name_about_org_index(filename):
    data = pd.read_json("teacher.json", lines=True)
    with open(filename, "w", encoding="UTF-8") as file:
        for i in range(len(data)):
            new_data = {"id": data["id"][i], "name": data["name"][i], "about": data["about"][i], "org": data["org_name"][i], "index": i}
            json.dump(new_data, file, separators=(", ", ":"), ensure_ascii=False)
            file.write(",\n")


# teacher.json数据量比较大，建议将数据写入文件中，而非返回dataFrame
def teacher_id_name_about_org_index_df():
    data = pd.read_json("teacher.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"id": data["id"][i], "name": data["name"][i], "about": data["about"][i], "org": data["org_name"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def cf_cid_cname_field_index(filename):
    data = pd.read_json("course-field.json", lines=True)
    with open(filename, "w", encoding="UTF-8") as file:
        for i in range(len(data)):
            new_data = {"cid": data["course_id"][i], "cname": data["course_name"][i], "field": data["field"][i], "index": i}
            json.dump(new_data, file, separators=(", ", ":"), ensure_ascii=False)
            file.write(",\n")


def cf_cid_cname_field_index_df():
    data = pd.read_json("course-field.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"cid": data["course_id"][i], "cname": data["course_name"][i], "field": data["field"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


# 获取course和field之间的关系并以字典形式返回
def get_relation_course_field():
    data = pd.read_json("course-field.json", lines=True)
    processed_data = {}
    for i in range(len(data)):
        processed_data[data["course_id"][i]] = data["field"][i]
    return processed_data

