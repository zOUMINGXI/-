import json
import pandas as pd
import numpy as np
# json文件的导入
def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df

# 统计每个用户选择的课程数目， 得出的结果主要包括 user_id, course_numbers
def count_user_course():
    user_and_course = read_json("../scripts/entities/user.json")
    user_choose_course = user_and_course[['id', 'course_order']]
    course = user_choose_course['course_order']
    course_numbers = list()
    for i in range(0,len(user_choose_course.index)):
        course_numbers.append(len(course.iloc[i]))
    # 这个copy()是为了避免使用原始列表出线报错
    user_choose_course_result = user_choose_course.copy()
    user_choose_course_result['course_numbers'] = course_numbers
    return user_choose_course_result

# print(count_user_course())