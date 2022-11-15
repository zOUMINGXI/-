import heapq
import math

import numpy as np


def eval_rating(rating_pred,test_data):
    # if rating_pred.shape != torch.Size([1246500]):
    #     rating_pred = rating_pred.squeeze(1)
    test_item_ids=test_data[1]
    test_batch_num = int(len(test_item_ids) / 50)
    # print(test_batch_num)22
    # print(rating_pred)
    # print(test_data[1])
    hits5, ndcgs5, hits10, ndcgs10, maps, mrrs = [], [], [], [], [], []
    for batch in range(test_batch_num):

        t_i=test_item_ids[batch*50:(batch+1)*50]
        predictions=rating_pred[batch*50:(batch+1)*50]
        # print(t_i)
        # print(predictions)
        map_item_score = {t_i[i]:predictions[i] for i in range(len(t_i))}
        gtItem = t_i[0]
        ranklist5 = heapq.nlargest(5, map_item_score, key=map_item_score.get)
        ranklist10 = heapq.nlargest(10, map_item_score, key=map_item_score.get)
        ranklist100 = heapq.nlargest(100, map_item_score, key=map_item_score.get)
        # print(ranklist10)
        hr5 = getHitRatio(ranklist5, gtItem)
        ndcg5 = getNDCG(ranklist5, gtItem)
        hr10 = getHitRatio(ranklist10, gtItem)
        ndcg10 = getNDCG(ranklist10, gtItem)
        ap = getAP(ranklist100, gtItem)
        mrr = getMRR(ranklist100, gtItem)
        hits5.append(hr5)
        ndcgs5.append(ndcg5)
        hits10.append(hr10)
        ndcgs10.append(ndcg10)
        maps.append(ap)
        mrrs.append(mrr)
        # print(hits10)
        final_hr5,final_hr10,final_ndcgs5,final_ndcgs10,final_map,final_mrr=np.array(hits5).mean(), np.array(hits10).mean(), np.array(ndcgs5).mean(), np.array(ndcgs10).mean(), np.array(maps).mean(), np.array(mrrs).mean()
    return final_hr5, final_hr10, final_ndcgs5, final_ndcgs10, final_map, final_mrr



def getHitRatio(ranklist, gtItem):
    for item in ranklist:
        if item == gtItem:
            return 1
    return 0


def getNDCG(ranklist, gtItem):
    for i in range(len(ranklist)):
        item = ranklist[i]
        if item == gtItem:
            return math.log(2) / math.log(i + 2)
    return 0


def getAP(ranklist, gtItem):
    hits = 0
    sum_precs = 0
    for n in range(len(ranklist)):
        if ranklist[n] == gtItem:
            hits += 1
            sum_precs += hits / (n + 1.0)
    if hits > 0:
        return sum_precs / 1
    else:
        return 0


def getMRR(ranklist, gtItem):
    for index, item in enumerate(ranklist):
        if item == gtItem:
            return 1.0 / (index + 1.0)
    return 0