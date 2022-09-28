import json
import pandas as pd
import matplotlib.pyplot as plt
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
    for i in range(0, len(user_choose_course.index)):
        course_numbers.append(len(course.iloc[i]))
    # 这个copy()是为了避免使用原始列表出线报错
    user_choose_course_result = user_choose_course.copy()
    user_choose_course_result['course_numbers'] = course_numbers
    return user_choose_course_result

course_chosen_by_users = count_user_course()

data = course_chosen_by_users['course_numbers']

bins = [0, 5, 15, 25, 35, 60, 100, 2000, 40000]

result = pd.cut(data, bins, right=True)

diff_blocks = pd.value_counts(result).sort_index()

# 直接通过plot.bar画出柱形图
diff_blocks.plot.bar(align='center')
# 显示每个柱的数据
for ax, ay in diff_blocks.reset_index().iterrows():
    plt.text(ax, ay.all(), '%s' % ay.iloc[1], size=10, ha='center', va='bottom', color='red')

# 图表标题 中文字体 需要加入fontname 即字体选择 SimHei 为中文字体
plt.title("用户选择课程数量分布", fontname="SimHei")

plt.show()

