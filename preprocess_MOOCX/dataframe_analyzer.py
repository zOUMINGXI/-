import pandas
import matplotlib.pyplot as plt
import numpy as np


# 必须是数字类型的数据才能画到图像里
def plot_dataframe(data):
    print("数据前5行为：", data.head(5))
    print("数据后5行为：", data.tail(5))
    print("数据索引为：", data.index)
    print("数据列为：", data.columns)
    print("数据值为：", data.values)
    print("数据描述为：", data.describe())
    print("数据平均值为：", data.mean())

    data.plot(kind='line')
    plt.show()


def attributes_of_dataframe(data):
    print("数据前5行为：", data.head(5))
    print("数据后5行为：", data.tail(5))

    print("数据索引为：", data.index)
    print("数据列为：", data.columns)
    print("数据值为：", data.values)

    print("数据描述为：", data.decscribe())

    print("数据平均值为：", data.mean())

    # print("某一列各个值出现的次数为：", data[colomn].value_counts())

    # data.apply(lambda x: x.max() - x.min()) 运行括号中的函数，括号中的函数表示返回最大值和最小值的差

    # 绘图

    data.pivot(index=None, columns=None, values=None)
    # 上面的函数对数据进行调整
    data.plot(x=None, y=None, kind='line',
              ax=None, subplots=False, sharex=None,
              sharey=False, layout=None,figsize=None,
              use_index=True, title=None, grid=None,
              legend=True, style=None, logx=False,
              logy=False, loglog=False, xticks=None,
              yticks=None, xlim=None, ylim=None,
              rot=None, xerr=None,secondary_y=False,
              sort_columns=False, **kwds)

    # 上面的函数作图
    # x : 横向标记位置,默认为None
    # y : 纵向标记位置,默认为None
    # kind 参数 : 绘制类型(字符串)
    # ‘kind=line’ : 折线图模式
    # ‘kind=bar’ : 纵向条形图模式
    # ‘kind=barh’ : 横向条形图模式
    # ‘kind=hist’ : 柱状图模式
    # ‘kind=box’ : 箱线图模式
    # ‘kind=kde’ : 密度估计图模式
    # ‘kind=area’ : 面积区域图模式
    # ‘kind=pie’ : 饼图模式
    # ‘kind=scatter’ : 散点图模式
    # ‘kind=hexbin’ : 蜂巢图模式
    # ax : 子图(如果没有设置，则使用当前matplotlib subplot**)
    # subplots : 图片中是否有子图,默认为False
    # sharex : 如果ax为None，则默认为True，否则为False
    # sharey : 默认为False如果有子图，子图共y轴刻度，标签
    # layout : 子图的行列布局
    # figsize : 图片尺寸大小
    # use_index : 默认为False,默认用索引做x轴
    # title : 图片的标题用字符串
    # grid : 默认为None,图片是否有网格
    # legend : 子图图例,默认为True
    # style : 每列折线图设置线的类型
    # logx : 默认为False,设置x轴刻度是否取对数
    # loglog : 默认为False,同时设置x，y轴刻度是否取对数
    # xticks : 设置x轴刻度值，序列形式
    # yticks : 设置y轴刻度值，序列形式
    # xlim : 设置坐标轴的范围
    # ylim : 设置坐标轴的范围
    # rot : 默认为None,设置轴标签的显示旋转度数
    # fontsize : 默认为None,设置轴刻度的字体大小
    # colormap : 默认为None,设置图的区域颜色
    # colorbar : 图片柱子
    # position : 取值范围[0,1],默认为0.5表示中间对齐,设置图的区域颜色
    # layout : 布局,几行几列
    # table : 默认为False,选择DataFrame类型的数据并且转换匹配matplotlib的布局
    # yerr : DataFrame, Series, array-like, dict and str
    # xerr : same types as yerr.
    # stacked : boolean, default False in line and
    # sort_columns : 默认为False,对列名称进行排序,默认使用前列顺序
    # secondary_y : 默认为False,是否要设置第二个Y轴
    # mark_right : 默认为True,在使用第二个Y轴时在Y轴上的标签
    plt.show()


# a.sort_index(axis=1,ascending=False)
# 其中axis=1表示对所有的columns进行排序，下面的数也跟着发生移动。
# 后面的ascending=False表示按降序排列，参数缺失时默认升序。

# a['x'] 那么将会返回columns为x的列
# a[0:3] 则会返回前三行的数据。

# loc是通过标签来选择数据
# a.loc['one']则会默认表示选取行为'one'的行；
# a.loc[:,['a','b'] ] 表示选取所有的行以及columns为a,b的列；
# a.loc[['one','two'],['a','b']] 表示选取'one'和'two'这两行以及columns为a,b的列；
# a.loc['one','a']与a.loc[['one'],['a']]作用是一样的，不过前者只显示对应的值，而后者会显示对应的行和列标签。

# iloc则是直接通过位置来选择数据
# 这与通过标签选择类似
# a.iloc[1:2,1:2] 则会显示第一行第一列的数据;(切片后面的值取不到)
# a.iloc[1:2] 即后面表示列的值没有时，默认选取行位置为1的数据;
# a.iloc[[0,2],[1,2]] 即可以自由选取行位置，和列位置对应的数据。

# 使用条件来选择
# 使用单独的列来选择数据
# a[a.c>0] 表示选择c列中大于0的数据
# 使用where来选择数据
# a[a>0] 表直接选择a中所有大于0的数据
# 使用isin()选出特定列中包含特定值的行
# a1=a.copy()
# a1[a1['one'].isin(['2','3'])] 表显示满足条件：列one中的值包含'2','3'的所有行。

# contact(a1,axis=0/1，keys=['xx','xx','xx',...])，其中a1表示要进行进行连接的列表数据,axis=1时表横着对数据进行连接。axis=0或不指定时，表将数据竖着进行连接。a1中要连接的数据有几个则对应几个keys，设置keys是为了在数据连接以后区分每一个原始a1中的数据。
# 例：a1=[b['a'],b['c']]
# result=pd.concat(a1,axis=1，keys=['1','2'])

# Append 将一行或多行数据连接到一个DataFrame上
# a.append(a[2:],ignore_index=True)
# 表示将a中的第三行以后的数据全部添加到a中，若不指定ignore_index参数，则会把添加的数据的index保留下来，若ignore_index=Ture则会对所有的行重新自动建立索引。

# merge类似于SQL中的join
# 设a1,a2为两个dataframe,二者中存在相同的键值，两个对象连接的方式有下面几种：
# (1)内连接，pd.merge(a1, a2, on='key')
# (2)左连接，pd.merge(a1, a2, on='key', how='left')
# (3)右连接，pd.merge(a1, a2, on='key', how='right')
# (4)外连接， pd.merge(a1, a2, on='key', how='outer')

# a.groupby(column) 根据column进行分组

# categories可以重新编码分类

