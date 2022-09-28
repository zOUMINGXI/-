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

# 以 用户对应课程数 为例
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

# 绘制柱形图
# 说明：data 需要特殊格式处理，输入为numbers的当列的dataframe
#      bins 输入想要的划分区间
#      title 为标题
def draw_count_user_course(data, bins, title: str):
    # 分割区间，这里的选择左开右闭区间
    result = pd.cut(data, bins, right=True)
    # 是一个显示每个区间数量的操作
    blocks_numbers = pd.value_counts(result).sort_index()
    blocks_numbers.plot.bar(align='center')
    # 标记、显示每个柱子的具体数量
    for ax, ay in blocks_numbers.reset_index().iterrows():

        plt.text(ax, ay.all(), '%s' % ay.iloc[1], size=10, ha='center', va='bottom', color='red')

    plt.title(title, fontname="SimHei")

    plt.show()
# 输入划分的区间
blocks = [0, 5, 15, 25, 35, 60, 100, 2000, 40000]
# 函数使用
draw_count_user_course(count_user_course()['course_numbers'], blocks, "用户选择课程数量分布")
