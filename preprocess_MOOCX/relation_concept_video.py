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

def get_relaton_concept_video():
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






