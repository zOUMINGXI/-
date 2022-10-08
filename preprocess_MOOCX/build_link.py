import json
import pandas as pd

# json文件的导入
def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df

# 处理特殊的格式 比如 带C_ 或者 U_
# def split_id():
    # course_id = read_json('../scripts/entities/course.json')['id']
    # course = course_id.str.replace('C_', '')
    # return print(course)

# 读取用户、课程、概念的数据各个的前100个
# 得出一个有 entity、item_id 的两个列的列表 其中item_id 仅是按读取行的顺序依次编号
# 其中用户读取了 user_id
# 课程读取了 course_id
# 概念读取了概念名 name
def link():
    # 读取用户ID
    user_id = read_json('../scripts/entities/user.json')['id'][0:100]
    # 读取课程ID
    course_id = read_json('../scripts/entities/course.json')['id'][0:100]
    # 读取概念名
    concept_id = read_json('../scripts/entities/concept.json')['name'][0:100]

    df_index = 0
    df = pd.DataFrame(columns=['entity', 'item_id'])
    for i in range(len(user_id.index)):
        df.loc[df_index] = [user_id.iloc[i], df_index]
        df_index += 1

    for i in range(len(course_id.index)):
        df.loc[df_index] = [course_id.iloc[i], df_index]
        df_index += 1

    for i in range(len(concept_id.index)):
        df.loc[df_index] = [concept_id.iloc[i], df_index]
        df_index += 1

    return df

