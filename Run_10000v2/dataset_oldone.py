##train
import numpy as np
import pandas as pd
import torch
from scipy.sparse import coo_matrix
from torch.utils.data import Dataset

class MyDataset_train(Dataset):
    def __init__(self,transform=None):
        self.transform=transform
        self.user_num=5000
        self.course_num=2509
        self.user2id={}#1
        self.id2user={}#1
        self.course2id={}#1
        self.id2course={}#1
        self.relation_num=0
        super(MyDataset_train, self).__init__()
        self.build()
    def load_inter(self,filepath='Data_5k/new_train_5000.inter'):
        df=pd.read_csv(filepath,encoding='utf-8',sep='\t',names=['user_id','course_id','rating'])
        # df.columns=['user_id','course_id','rating']
        return df
    def load_link_user(self,filepath='Data_5k/new_5000_user.link'):
        df=pd.read_csv(filepath,encoding='utf-8',sep='\t',names=['item_id','entity_id'])
        # df.columns=['item_id','entity_id']
        return df
    def load_link_course(self,filepath='Data_5k/new_5000_course.link'):
        df=pd.read_csv(filepath,encoding='utf-8',sep='\t',names=['item_id','entity_id'])
        return df
    def load_kg(self,filepath='Data_5k/new_5000.kg'):
        df=pd.read_csv(filepath,encoding='utf-8',sep='\t',names=['head_id','relation','tail_id'])
        # df.columns=['head_id','relation','tail_id']
        return df
    def num_users(self):
        return self.user_num
    def num_course(self):
        return self.course_num
    def num_entity(self):
        return  self.course_num+self.user_num
    def num_relation(self):
        return self.relation_num
    def build(self):
        for line in open('Data_5k/new_5000_user.link',encoding='utf-8').readlines()[0:]:
            # print(line.split())
            user,user_id=line.split()
            self.user2id[user]=user_id
            self.id2user[user_id]=user

        for line in open('Data_5k/new_5000_course.link',encoding='utf-8').readlines()[0:]:
            course,course_id=line.split()
            self.course2id[course]=course_id
            self.id2course[course_id]=course

        self.relation_num=self.load_kg().shape[0]
        self.df_inter=self.load_inter()
        # print(len(self.df_inter))
        self.df_kg=self.load_kg()
        # print(self.df_kg['relation'])
        self.users=self.load_link_user()['entity_id']
        self.courses=self.load_link_course()['entity_id']
        self.head_entity=self.df_kg['head_id'].to_numpy()#正采样user_id、图头实体
        self.tail_entity=self.df_kg['tail_id'].to_numpy()#正采样course_id，图尾实体
        self.relation=self.df_kg['relation'].to_numpy()
    def entity_num(self):
        return self.course_num+self.user_num
    def create_ckg_sparse_matrix(self):
        kg=self.df_kg
        inter=self.df_inter
        user_num=self.user_num

        user=inter['user_id'].numpy()
        item=inter['course_id'].numpy()
        user_len=len(user)#共多少交互信息
        src=torch.cat([user,item,self.head_entity])
        tgt=torch.cat([item,user,self.tail_entity])
        rel_id=self.relation_num-1
        kg_rel=kg['relation'].numpy()
        ui_rel=np.full(2*user_len,rel_id,dtype=np.str)
        data=np.concatenate([ui_rel,kg_rel])
        node_num=user_num+self.course_num
        mat = coo_matrix((data, (src, tgt)), shape=(node_num, node_num))
        return mat

    def kg_graph(self):
        return self.create_ckg_sparse_matrix()
    def __getitem__(self, index):
        df=self.df_inter.iloc[index]
        sample=(df[0],df[1],df[2])
        return sample
    def __len__(self):
        return len(self.df_inter)
    def history_item_matrix(self):
        user_ids=self.df_inter['user_id'].to_numpy()
        item_ids=self.df_inter['course_id'].to_numpy()
        labels=self.df_inter['rating'].to_numpy()
        ##youdianwenticao
        row_num, max_col_num = self.user_num+500, self.course_num
        row_ids, col_ids = user_ids, item_ids
        history_len = np.zeros(row_num, dtype=np.int64)
        for row_id in row_ids:
            history_len[row_id] += 1
        col_num = np.max(history_len)
        history_matrix = np.zeros((row_num, col_num), dtype=np.int64)
        history_value = np.zeros((row_num, col_num))
        history_len[:] = 0
        for row_id, label, col_id in zip(row_ids, labels, col_ids):
            history_matrix[row_id, history_len[row_id]] = col_id
            history_value[row_id, history_len[row_id]] = label
            history_len[row_id] += 1
        return torch.LongTensor(history_matrix), torch.FloatTensor(history_value), torch.LongTensor(history_len)





