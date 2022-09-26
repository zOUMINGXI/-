import pandas as pd
import json


def get_relation_course_field():
    data = pd.read_json("course-field.json", lines=True)
    return data


def get_relation_course_field_csv(data):
    data.to_csv("get_relation_course_field.csv", mode="w", index=False)


get_relation_course_field_csv(get_relation_course_field())
