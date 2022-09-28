import json
import pandas as pd

# json文件的导入
def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df

# 该函数得出以用户与课程一对一关系
def user_to_course():
    user_and_course = read_json("../scripts/entities/user.json")
    # 这里只取前100个数据
    user_choose_course = user_and_course[['id', 'course_order']][0:100]
    df = pd.DataFrame(columns=['id', 'course_order', 'rating'])
    df_index = 0
    for i in range(len(user_choose_course.index)):
        course_id = user_choose_course['id'].iloc[i]
        courses = user_choose_course['course_order'].iloc[i]
        for j in range(len(courses)):
            df.loc[df_index] = [course_id, courses[j], 1]
            df_index += 1
    return df

# print(user_to_course())
