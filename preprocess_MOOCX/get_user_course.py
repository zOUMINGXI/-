import json
import random

import numpy as np
import pandas as pd
import time
import re
import sys
import codecs
import pickle

batch = 10000


def read_json(file, count=10000):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        if count < len(data) - batch:
            data = list(map(json.loads, data[count:count + batch]))
        elif len(data) - batch <= count < len(data):
            data = list(map(json.loads, data[count:]))
        else:
            return None
        df = pd.DataFrame(data)
        f.close()
        return df


def get_user_course_relation(count=10000):  # index:id:course_order
    data = read_json("user.json", count)
    if data is not None:
        data = data[["id", "course_order"]].reset_index()
    return data


# 此函数生成csv文件
def get_user_course_relation_csv(data):
    data.to_csv("get_user_course_relation.csv", mode="w", index=False)


# 此函数生成pickle文件
def get_user_course_relation_pickle(data):
    data.to_pickle("get_user_course_relation.pkl")


# 从link文件中获取对应的实体名
# link_path link文件路径, item_id 搜寻的实体id
def get_entity_name(link_path, item_id):
    with open(link_path, "r", encoding="UTF-8") as link_file:
        i = 0
        while True:
            data = link_file.readline()
            if not data:
                link_file.close()
                return None
            else:
                if i < 0:
                    i += 1
                else:
                    data = data.split("\t")
                    if data[0] == item_id:
                        link_file.close()
                        return data[1].split("\n")[0]
                    else:
                        i += 1


# left user实体link文件， right course实体link文件
def get_user_course_relation_KG(left_link_path, right_link_path, data):
    with open("test_2000_user_course_relation.kg", "w", encoding="UTF-8") as file:
        for i in range(len(data["id"])):
            # if i >= 2:
            #     break
            # print(data["id"][i])
            # print(data["course_order"][i])
            left_name = get_entity_name(left_link_path, data["id"][i])
            print(left_name)
            for j in range(len(data["course_order"][i])):
                # 某用户选择了某课程
                right_name = get_entity_name(right_link_path, str(data["course_order"][i][j]))
                print(right_name)
                if left_name is None:
                    continue
                if right_name is None:
                    continue
                file.write(left_name)
                file.write("\t")
                # 关系id规则不太明确，如果出问题可以自行修改
                file.write("1")  # 1 present user takes course
                file.write("\t")
                file.write(right_name)
                file.write("\n")
                file.write(right_name)
                file.write("\t")
                # 关系id规则不太明确，如果出问题可以自行修改
                file.write("2")  # 2 present course taken by user
                file.write("\t")
                file.write(left_name)
                file.write("\n")
        file.close()


flag = []
user_flag = []


def get_user_course_relation_link(data):
    with open("test_2000_user_course_relation.link", "w", encoding="UTF-8") as file:
        count = 13177
        for i in range(len(data["id"])):
            file.write(data["id"][i])
            file.write("\t")
            file.write(str(count))
            file.write("\n")
            count += 1
        for i in range(len(data["course_order"])):
            for j in range(len(data["course_order"][i])):
                if data["course_order"][i][j] not in flag:
                    file.write(str(data["course_order"][i][j]))
                    file.write("\t")
                    file.write(str(count))
                    file.write("\n")
                    count += 1
                    flag.append(data["course_order"][i][j])
        file.close()


def get_link_of_large_data():
    count = 0
    data = get_user_course_relation(count)
    id_count = 0
    while data is not None:
        for i in range(len(data["course_order"])):
            for j in range(len(data["course_order"][i])):
                if data["course_order"][i][j] not in flag:
                    flag.append(data["course_order"][i][j])
        print("     flag: ", len(flag))
        with open("test_all_user_course_relation.link", "a", encoding="UTF-8") as file:
            for i in range(len(data["id"])):
                file.write(data["id"][i])
                file.write("\t")
                file.write(str(id_count))
                file.write("\n")
                id_count += 1
            file.close()
        count += batch
        data = get_user_course_relation(count)
    with open("test_all_user_course_relation.link", "a", encoding="UTF-8") as file:
        for i in range(len(flag)):
            file.write(str(flag[i]))
            file.write("\t")
            file.write(str(id_count))
            file.write("\n")
            id_count += 1
        file.close()


def get_kg_of_large_data():
    count = 0
    data = get_user_course_relation(count)
    while data is not None:
        get_user_course_relation_KG("test_all_user_course_relation.link", "test_all_user_course_relation.link", data)
        count += batch
        data = get_user_course_relation(count)


def to_entity_id(origin_file, link_file):
    with open("eid_" + origin_file, "w", encoding="UTF-8") as target_file:
        with open(origin_file, "r", encoding="UTF-8") as res_file:
            data = res_file.readlines()
            for item in data:
                user_course_rating_str = ""
                user_course_rating_list = item.split("\t")
                user = get_entity_name(link_file, user_course_rating_list[0])
                if user:
                    user_course_rating_str += user
                    user_course_rating_str += "\t"
                else:
                    user_course_rating_str += user_course_rating_list[0]
                    user_course_rating_str += "\t"

                course = get_entity_name(link_file, user_course_rating_list[1])
                if course:
                    user_course_rating_str += course
                    user_course_rating_str += "\t"
                else:
                    user_course_rating_str += user_course_rating_list[1]
                    user_course_rating_str += "\t"

                user_course_rating_str += user_course_rating_list[2]

                target_file.write(user_course_rating_str)


def get_user_course_inter(kg_path, link_path, inter_path):
    with open(inter_path, "w", encoding="UTF-8") as inter_file:
        with open(kg_path, "r", encoding="UTF-8") as kg_file:
            kg_data = kg_file.readlines()
            with open(link_path, "r", encoding="UTF-8") as link_file:
                link_data = link_file.readlines()
                samples = []
                for item in link_data:
                    entity_id = item.split("\t")
                    entity = entity_id[0]
                    id = entity_id[1].split("\n")[0]
                    if not re.match(r'U_.*', entity):
                        samples.append(id)

                user_course_dict = {}
                for item in kg_data:
                    user_relation_course = item.split("\t")
                    user = user_relation_course[0]
                    user_course_dict[user] = []
                for item in kg_data:
                    user_relation_course = item.split("\t")
                    user = user_relation_course[0]
                    course = user_relation_course[2].split("\n")[0]
                    user_course_dict[user].append(course)

                sample_user_course_dict = {}
                for user, course in user_course_dict.items():
                    sample_user_course_dict[user] = []
                    for i in range(len(course)):
                        while True:
                            rand_int = random.randint(0, len(samples) - 1)
                            if samples[rand_int] not in course:
                                sample_user_course_dict[user].append(samples[rand_int])
                                break

                # print(samples[0:100])
                # print(user_course_dict["9999"])
                # print(sample_user_course_dict["9999"])
                for user, course in user_course_dict.items():
                    for item in course:
                        inter_file.write(user)
                        inter_file.write("\t")
                        inter_file.write(item)
                        inter_file.write("\t1\n")
                    for item in sample_user_course_dict[user]:
                        inter_file.write(user)
                        inter_file.write("\t")
                        inter_file.write(item)
                        inter_file.write("\t0\n")


def split_user_and_course(link_path):
    with open(link_path, "r", encoding="UTF-8") as origin:
        with open("origin_10000_user.link", "a", encoding="UTF-8") as user:
            with open("origin_10000_course.link", "a", encoding="UTF-8") as course:
                data = origin.readline()
                while data:
                    if re.match(r'U_.*', data):
                        user.write(data)
                    else:
                        course.write(data)
                    data = origin.readline()


def split_inter(inter_path):
    with open(inter_path, "r", encoding="UTF-8") as file:
        with open("origin_10000p_user_course_relation.inter", "w", encoding="UTF-8") as target:
            data = file.readline()
            while data:
                arr = data.split("\t")
                arr[2] = arr[2].split("\n")[0]
                if arr[2] == "1":
                    target.write(data)
                data = file.readline()


def select_user_course_into_files(least=5, most=10, kgpath="test.kg", onewayKg="test_oneway.kg", linkpath="test_unsorted.link", dataSize=12000):
    with open(kgpath, "w", encoding="UTF-8") as kg:
        with open(linkpath, "w", encoding="UTF-8") as link:
            with open(onewayKg, "w", encoding="UTF-8") as oneway:

                dataset_num = 0

                user_id = 12960
                course_id = dataSize + 12960

                courses = dict()

                count = 0

                data = get_user_course_relation(count)
                while data is not None:
                    for i in range(len(data["id"])):
                        if least <= len(data["course_order"][i]) <= most:
                            if dataset_num < 10010:
                                dataset_num += 1
                                continue

                            link.write(data["id"][i])
                            link.write("\t")
                            link.write(str(user_id))
                            link.write("\n")

                            for item in data["course_order"][i]:
                                if item not in courses:
                                    courses[item] = course_id

                                    link.write(str(item))
                                    link.write("\t")
                                    link.write(str(course_id))
                                    link.write("\n")

                                    kg.write(str(user_id))
                                    kg.write("\t")
                                    kg.write("1\t")
                                    kg.write(str(course_id))
                                    kg.write("\n")

                                    kg.write(str(course_id))
                                    kg.write("\t")
                                    kg.write("2\t")
                                    kg.write(str(user_id))
                                    kg.write("\n")

                                    oneway.write(str(user_id))
                                    oneway.write("\t")
                                    oneway.write("1\t")
                                    oneway.write(str(course_id))
                                    oneway.write("\n")

                                    course_id += 1
                                else:
                                    this_course_id = courses[item]

                                    kg.write(str(user_id))
                                    kg.write("\t")
                                    kg.write("1\t")
                                    kg.write(str(this_course_id))
                                    kg.write("\n")

                                    kg.write(str(this_course_id))
                                    kg.write("\t")
                                    kg.write("2\t")
                                    kg.write(str(user_id))
                                    kg.write("\n")

                                    oneway.write(str(user_id))
                                    oneway.write("\t")
                                    oneway.write("1\t")
                                    oneway.write(str(this_course_id))
                                    oneway.write("\n")

                            user_id += 1

                            dataset_num += 1
                            if dataset_num >= dataSize + 10010:
                                return dataset_num

                    count += batch
                    data = get_user_course_relation(count)


def sort_link(linkpath="test_unsorted.link", sortedlinkpath="test.link"):
    with open(linkpath, "r", encoding="UTF-8") as file:
        with open(sortedlinkpath, "w", encoding="UTF-8") as sortlink:
            data = file.readlines()
            entities = dict()
            for item in data:
                entity_id = item.split("\t")
                print(entity_id)
                entity_id[1] = entity_id[1].split("\n")[0]
                entities[entity_id[0]] = int(entity_id[1])

            sorted_entities = sorted(entities.items(), key=lambda x: x[1])
            for item in sorted_entities:
                # print(item[0], item[1])
                sortlink.write(item[0])
                sortlink.write("\t")
                sortlink.write(str(item[1]))
                sortlink.write("\n")





# raw_data = get_user_course_relation()
# get_user_course_relation_link(raw_data)
# get_user_course_relation_KG("test_2000_user_course_relation.link", "test_2000_user_course_relation.link", raw_data)
# get_user_course_inter("test_2000_user_course_relation_oneway.kg", "test_2000_user_course_relation.link")
# split_user_and_course("test_2000_user_course_relation.link")
# split_inter("test_2000_user_course_relation.inter")
# select_user_course_into_files(5, 10, "origin_10000.kg","origin_10000_oneway.kg", "origin_10000.link", 10000)
# sort_link("origin_10000.link", "origin_10000_sorted.link")
# get_user_course_inter("origin_10000_oneway.kg", "origin_10000.link", "origin_10000.inter")

# select_user_course_into_files(5, 10, "origin_2000.kg","origin_2000_oneway.kg", "origin_2000.link", 2000)
# sort_link("origin_2000.link", "origin_2000_sorted.link")
# get_user_course_inter("origin_2000_oneway.kg", "origin_2000.link", "origin_2000.inter")

# split_inter("origin_10000.inter")
# split_user_and_course("origin_10000.link")
