import pandas as pd
import json


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


# 此函数用于输出csv文件，大小可能达到5GB
def get_relation_user_video_csv():
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
            new_data = dict()
            new_data[data["user_id"]] = video_id
            if i == 0:
                df = pd.DataFrame.from_dict(new_data, orient="index")
                df.to_csv("get_relation_user_video.csv", mode="w", index=False)
            else:
                df = pd.DataFrame.from_dict(new_data, orient="index")
                df.to_csv("get_relation_user_video.csv", mode="a", index=False, header=False)
            i = i + 1


get_relation_user_video_csv()
