##test
from torch.utils.data import Dataset
import numpy as np
import pandas as pd
import torch
from scipy.sparse import coo_matrix

class MyDataset_test(Dataset):
    def __init__(self,transform=None):
        self.transform=transform
        self.user_num=5000
        self.course_num=2509
        self.user2id={}#1
        self.id2user={}#1
        self.course2id={}#1
        self.id2course={}#1
        self.relation_num=0
        super(MyDataset_test, self).__init__()
        self.build()
    def load_inter(self,filepath='Data_5k/new_test_5000.inter'):
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

            user,user_id=line.split()
            self.user2id[user]=user_id
            self.id2user[user_id]=user

        for line in open('Data_5k/new_5000_course.link',encoding='utf-8').readlines()[0:]:
            course,course_id=line.split()
            self.course2id[course]=course_id
            self.id2course[course_id]=course

        self.relation_num=self.load_kg().shape[0]
        self.df_inter=self.load_inter()
        self.df_kg=self.load_kg()
        self.users=self.load_link_user()['entity_id']
        self.courses=self.load_link_course()['entity_id']
        self.relation=self.df_kg['relation'].to_numpy()
    def entity_num(self):
        return self.course_num+self.user_num
    def create_ckg_sparse_matrix(self):
        kg=self.df_kg
        inter=self.df_inter
        user_num=self.user_num
        self.head_entity=kg['head_id'].numpy()
        self.tail_entity=kg['tail_id'].numpy()
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
    def get_test_set(self):
        test_user_ids,test_course_ids,test_rating=[],[],[]
        for i in range(len(self.df_inter)):
            test_user_ids.append(self.df_inter['user_id'].iloc[i])
            test_course_ids.append(self.df_inter['course_id'].iloc[i])
            test_rating.append(self.df_inter['rating'].iloc[i])
        return [torch.LongTensor(test_user_ids),torch.LongTensor(test_course_ids),torch.LongTensor(test_rating)]
