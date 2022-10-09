import pandas as pd
import json
import pickle


# 此函数用于输出json文件
def get_relation_user_video_index(file_name):
    with open("user-video.json", "r", encoding="UTF-8") as file:
        with open(file_name, "w", encoding="UTF-8") as write_file:
            i = 0
            while True:
                line = file.readline()
                if not line:
                    break
                data = json.loads(line)
                video_id = []
                for j in range(len(data["seq"])):
                    video_id.append(data["seq"][j]["video_id"])
                new_data = {"video_id": video_id, "user_id": data["user_id"], "index": i}
                i = i + 1
                json.dump(new_data, write_file, separators=(", ", ":"), ensure_ascii=False)
                write_file.write(",\n")


# 此函数用于输出csv文件
def get_relation_user_video_csv():
    with open("user-video.json", "r", encoding="UTF-8") as file:
        i = 0
        while True:
            line = file.readline()
            # 可以在下方if后面再添加一个i >= 100做测试
            if not line:
                break
            data = json.loads(line)
            video_id = []
            for j in range(len(data["seq"])):
                video_id.append(data["seq"][j]["video_id"])
            new_data = dict({"user_id": data["user_id"], "video_id": video_id})
            if i == 0:
                df = pd.DataFrame.from_dict(new_data, orient="index")
                df.to_csv("get_relation_user_video.csv", mode="w", index=False)
            else:
                df = pd.DataFrame.from_dict(new_data, orient="index")
                df.to_csv("get_relation_user_video.csv", mode="a", index=False, header=False)
            i = i + 1


# 此函数用于生成pickle格式文件
def get_relation_user_video_pickle():
    with open("user-video.json", "r", encoding="UTF-8") as file:
        i = 0
        while True:
            line = file.readline()
            if not line:
                break
            data = json.loads(line)
            video_id = []
            for j in range(len(data["seq"])):
                video_id.append(data["seq"][j]["video_id"])
            new_data = dict({"user_id": data["user_id"], "video_id": video_id})
            if i == 0:
                df = pd.DataFrame.from_dict(new_data, orient="index")
                # df.to_pickle("get_relation_user_video.pkl")
                with open("get_relation_user_video.pkl", "wb") as pickle_file:
                    pickle.dump(df, pickle_file)
            else:
                df = pd.DataFrame.from_dict(new_data, orient="index")
                with open("get_relation_user_video.pkl", "ab") as pickle_file:
                    pickle.dump(df, pickle_file)
            i = i + 1


# 从link文件中获取对应的实体名
# link_path link文件路径, item_id 搜寻的实体id
def get_entity_name(link_path, item_id):
    with open(link_path, "r", encoding="UTF-8") as link_file:
        i = 0
        while True:
            data = link_file.readline()
            if not data:
                return None
            else:
                if i == 0:
                    i += 1
                else:
                    data = data.split("\t")
                    if data[0] == item_id:
                        return data[1]
                    else:
                        i += 1


# left user实体link文件， right video实体link文件
# 此函数用于生成KG格式文件
def get_relation_user_video_KG(left_link_path, right_link_path):
    with open("user-video.json", "r", encoding="UTF-8") as file:
        with open("relation_user_video.kg", "w", encoding="UTF-8") as writing_file:
            writing_file.write("head_id:token\trelation_id:token\ttail_id:token\n")
            i = 0
            while True:
                line = file.readline()
                if not line or i >= 100:
                    break
                data = json.loads(line)
                for j in range(len(data["seq"])):
                    # 某用户看了某视频
                    writing_file.write(get_entity_name(left_link_path, data["user_id"]))
                    writing_file.write("\t")
                    # 关系id规则不太明确，如果出问题可以自行修改
                    writing_file.write("user.user.watch_videos")
                    writing_file.write("\t")
                    writing_file.write(get_entity_name(right_link_path, data["seq"][j]["video_id"]))
                    writing_file.write("\n")
                    # 某视频被某用户看过
                    writing_file.write(get_entity_name(right_link_path, data["seq"][j]["video_id"]))
                    writing_file.write("\t")
                    writing_file.write("video.video.watched_by")
                    writing_file.write("\t")
                    writing_file.write(get_entity_name(left_link_path, data["user_id"]))
                    writing_file.write("\n")
                i = i + 1


# 此函数用于生成LINK格式文件（以老范的为准吧，我这个link函数随便写的，但是又觉得某些地方以后用得上）
# def get_relation_user_video_link():
#     with open("user-video.json", "r", encoding="UTF-8") as file:
#         with open("relation_user_video.link", "w", encoding="UTF-8") as writing_file:
#             writing_file.write("item_id:token\tentity_id:token\n")
#             i = 0
#             while True:
#                 line = file.readline()
#                 if not line or i >= 100:
#                     break
#                 data = json.loads(line)
#                 for j in range(len(data["user_id"])):
#                     # watch_time = 0
#                     # segment = data["seq"][j]["segment"]
#                     # for i in range(len(segment)):
#                     #     if segment[i]["end_point"] >= segment[i]["start_point"]:
#                     #         watch_time = watch_time + segment[i]["end_point"] - segment[i]["start_point"]
#                     writing_file.write(data["user_id"])
#                     writing_file.write("\t")
#                     user_id = list(data["user_id"])
#                     user_id.pop(0)
#                     user_id.pop(0)
#                     user_id = int("".join(user_id))
#                     writing_file.write(user_id)
#                     writing_file.write("\n")
#                 i = i + 1

