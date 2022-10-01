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


# get_relation_user_video_index("video_user_index.json")


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


# get_relation_user_video_csv()


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


# get_relation_user_video_pickle()
# pic = pd.read_pickle("get_relation_user_video.pkl")
# print(pic)


# 此函数用于生成KG格式文件
def get_relation_user_video_KG():
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
                    # watch_time = 0
                    # segment = data["seq"][j]["segment"]
                    # for i in range(len(segment)):
                    #     if segment[i]["end_point"] >= segment[i]["start_point"]:
                    #         watch_time = watch_time + segment[i]["end_point"] - segment[i]["start_point"]
                    writing_file.write("users." + data["user_id"])
                    writing_file.write("\t")
                    # writing_file.write(str(abs(int(watch_time / 10))))
                    writing_file.write("users.user.watch_video")
                    writing_file.write("\t")
                    writing_file.write(data["seq"][j]["video_id"])
                    writing_file.write("\n")
                i = i + 1


# get_relation_user_video_KG()


# 此函数用于生成LINK格式文件
def get_relation_user_video_link():
    with open("user-video.json", "r", encoding="UTF-8") as file:
        with open("relation_user_video.link", "w", encoding="UTF-8") as writing_file:
            writing_file.write("item_id:token\tentity_id:token\n")
            i = 0
            while True:
                line = file.readline()
                if not line or i >= 100:
                    break
                data = json.loads(line)
                for j in range(len(data["user_id"])):
                    # watch_time = 0
                    # segment = data["seq"][j]["segment"]
                    # for i in range(len(segment)):
                    #     if segment[i]["end_point"] >= segment[i]["start_point"]:
                    #         watch_time = watch_time + segment[i]["end_point"] - segment[i]["start_point"]
                    writing_file.write(data["user_id"])
                    writing_file.write("\t")
                    writing_file.write("users." + data["user_id"])
                    writing_file.write("\n")
                i = i + 1

