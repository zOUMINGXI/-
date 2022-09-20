import pandas as pd
import json


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


def video_ccid_name_text_index_df():
    data = pd.read_json("video.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"ccid": data["ccid"][i], "name": data["name"][i], "text": data["text"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def problem_pid_title_content_option_index_df():
    data = pd.read_json("problem.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"problem_id": data["problem_id"][i], "title": data["title"][i], "content": data["content"][i], "option": data["option"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def school_id_name_index_df():
    data = pd.read_json("school.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"id": data["id"][i], "name": data["name"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def teacher_id_name_about_org_index_df():
    data = pd.read_json("teacher.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"id": data["id"][i], "name": data["name"][i], "about": data["about"][i], "org": data["org_name"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


def cf_cid_cname_field_index_df():
    data = pd.read_json("course-field.json", lines=True)
    new_dataframe = []
    for i in range(len(data)):
        new_data = {"cid": data["course_id"][i], "cname": data["course_name"][i], "field": data["field"][i], "index": i}
        new_dataframe.append(new_data)
    return pd.DataFrame(new_dataframe)


# print(type(course_id_name_field_index_df()))
# print(type(video_ccid_name_text_index_df()))
print(type(problem_pid_title_content_option_index_df()))
# print(type(school_id_name_index_df()))
# print(type(teacher_id_name_about_org_index_df()))
# print(type(cf_cid_cname_field_index_df()))
