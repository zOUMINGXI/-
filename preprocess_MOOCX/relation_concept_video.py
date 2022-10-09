import json
import pandas as pd


# json文件的导入
def read_json(file):
    with open(file, "r", encoding='utf-8') as f:
        data = f.readlines()
        data = list(map(json.loads, data))
    df = pd.DataFrame(data)
    return df


# course.json 中 ‘resource’ 词条 中的 resource_id -> course_id
# ‘resource_id’ 在 video_iod-ccid.txt 中 'ccid' -> ‘video_id’('resource_id')
#  'ccid'  在 concept-video.txt 中 'id' -> 'ccid'

def get_relation_concept_video():
    # 载入概念的词条
    concepts = read_json("../scripts/entities/concept.json")
    concepts_dict = concepts[['id', 'name']]
    # 调用其他原始数据
    concept_id_video = pd.read_csv("../scripts/relations/concept-video.txt", sep='\t', names=['id', 'ccid'])
    video_id_ccid = pd.read_csv("../scripts/relations/video_id-ccid.txt", sep='\t', names=['video_id', 'ccid'])
    concept_id_video_id = pd.merge(concept_id_video, video_id_ccid, how='inner', on='ccid')
    # 与原始的概念 数据合并
    relation = pd.merge(concepts_dict, concept_id_video_id, how='inner', on='id')
    get_relation = relation[['id', 'video_id']]
    return get_relation


def get_relation_concept_video_csv(get_relation):
    get_relation.to_csv("get_relation_concept_video.csv", mode="w", index=False)


# 此函数生成pickle文件
def get_relation_concept_video_pickle(data):
    data.to_pickle("get_relation_concept_video.pkl")

# get_relation_concept_video_csv(get_relation_concept_video())


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


# left concept实体link文件， right video实体link文件
def get_relation_concept_video_KG(left_link_path, right_link_path, data):
    with open("relation_concept_video.kg", "w", encoding="UTF-8") as file:
        file.write("head_id:token\trelation_id:token\ttail_id:token\n")
        for i in range(len(data["id"])):
            if i >= 100:
                break
            left_name = get_entity_name(left_link_path, data["id"][i])
            if left_name is None:
                continue
            for j in range(len(data["video_id"][i])):
                right_name = get_entity_name(right_link_path, data["video_id"][i][j])
                if right_name is None:
                    continue
                # 某概念与某视频相关
                file.write(left_name)
                file.write("\t")
                # 关系id规则不太明确，如果出问题可以自行修改
                file.write("concept.concept.related_videos")
                file.write("\t")
                file.write(right_name)
                file.write("\n")
                # 某视频与某概念相关
                file.write(right_name)
                file.write("\t")
                file.write("video.video.for_concept")
                file.write("\t")
                file.write(left_name)
                file.write("\n")


# def get_relation_concept_video_link(data):
#     with open("get_relation_concept_video.link", "w", encoding="UTF-8") as file:
#         file.write("item_id:token\tentity_id:token\n")
#         for i in range(len(data["id"])):
#             if i >= 100:
#                 break
#             file.write(data["id"])
#             file.write("\t")
#             file.write("concepts." + data["id"][i])
#             file.write("\n")
