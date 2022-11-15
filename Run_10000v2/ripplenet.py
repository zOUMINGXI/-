import collections
import numpy as np
import torch
import torch.nn as nn

from recbole.model.init import xavier_normal_initialization
from recbole.model.loss import BPRLoss, EmbLoss


class RippleNet(nn.Module):

    input_type = 1

    def __init__(self, dataset):
        self.device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        super(RippleNet, self).__init__()
        self.n_users = dataset.num_users()
        self.n_items = dataset.num_course()
        self.n_entities = dataset.num_entity()
        self.n_relations = dataset.num_relation()
        self.lr=0.0012
        # load dataset info
        # load parameters info
        self.embedding_size = 64
        self.kg_weight =0.01
        self.reg_weight = 1e-7
        self.n_hop = 2
        self.n_memory = 16
        head_entities = dataset.head_entity.tolist()
        tail_entities = dataset.tail_entity.tolist()
        relations = dataset.relation.tolist()
        kg = {}
        for i in range(len(head_entities)):
            head_ent = head_entities[i]
            tail_ent = tail_entities[i]
            relation = relations[i]
            kg.setdefault(head_ent, [])
            kg[head_ent].append((tail_ent, relation))
        self.kg = kg
        users = dataset.load_inter()['user_id'].tolist()
        items = dataset.load_inter()['course_id'].tolist()
        ratings=dataset.load_inter()['rating'].tolist()
        user_dict = {}
        for i in range(len(users)):
            user = users[i]
            item = items[i]
            user_dict.setdefault(user, [])#if user_dict[user] don`t exsit,user_dict[user]=[]
            if(ratings[i]==1):#貌似这个字典只要正样本
                user_dict[user].append(item)
        self.user_dict = user_dict
        self.ripple_set = self._build_ripple_set()

        # define layers and loss
        self.entity_embedding = nn.Embedding(self.n_entities, self.embedding_size).to(self.device)
        self.relation_embedding = nn.Embedding(self.n_relations, self.embedding_size * self.embedding_size).to(self.device)
        self.transform_matrix = nn.Linear(self.embedding_size, self.embedding_size, bias=False).to(self.device)
        self.softmax = torch.nn.Softmax(dim=1)
        self.sigmoid = torch.nn.Sigmoid()
        self.rec_loss = BPRLoss()
        self.l2_loss = EmbLoss()
        self.loss = nn.BCEWithLogitsLoss()

        # parameters initialization
        self.apply(xavier_normal_initialization)
        self.other_parameter_name = ['ripple_set']

    def _build_ripple_set(self):
        r"""Get the normalized interaction matrix of users and items according to A_values.
        Get the ripple hop-wise ripple set for every user, w.r.t. their interaction history

        Returns:
            ripple_set (dict)
        """
        ripple_set = collections.defaultdict(list)#if key don`t exsit,return list()

        n_padding = 0
        for user in self.user_dict:
            for h in range(self.n_hop):
                #
                memories_h = []
                memories_r = []
                memories_t = []

                if h == 0:
                    # print(1)
                    tails_of_last_hop = self.user_dict[user]#正采样的课程
                    # print(self.user_dict[user])
                else:

                    tails_of_last_hop = ripple_set[user][-1][2]

                for entity in tails_of_last_hop:#entity是course
                    # print(entity)
                    # print('已执行1')
                    # print(entity)
                    if entity not in self.kg:
                        # print(entity)
                        # print(self.kg)
                        continue
                    # print(self.kg[entity])
                    for tail_and_relation in self.kg[entity]:
                        # print(entity,tail_and_relation)
                        memories_h.append(entity)
                        memories_r.append(tail_and_relation[1])
                        memories_t.append(tail_and_relation[0])

                # if the current ripple set of the given user is empty,
                # we simply copy the ripple set of the last hop here
                if len(memories_h) == 0:
                    if h == 0:
                        # self.logger.info("user {} without 1-hop kg facts, fill with padding".format(user))
                        # raise AssertionError("User without facts in 1st hop")
                        n_padding += 1
                        memories_h = [0 for _ in range(self.n_memory)]
                        memories_r = [0 for _ in range(self.n_memory)]
                        memories_t = [0 for _ in range(self.n_memory)]
                        memories_h = torch.LongTensor(memories_h)
                        memories_r = torch.LongTensor(memories_r)
                        memories_t = torch.LongTensor(memories_t)
                        ripple_set[user].append((memories_h, memories_r, memories_t))
                    else:
                        ripple_set[user].append(ripple_set[user][-1])
                else:
                    # sample a fixed-size 1-hop memory for each user
                    replace = len(memories_h) < self.n_memory #true
                    #
                    indices = np.random.choice(len(memories_h), size=self.n_memory, replace=replace)
                    memories_h = [memories_h[i] for i in indices]
                    memories_r = [memories_r[i] for i in indices]
                    memories_t = [memories_t[i] for i in indices]
                    memories_h = torch.LongTensor(memories_h)
                    memories_r = torch.LongTensor(memories_r)
                    memories_t = torch.LongTensor(memories_t)
                    ripple_set[user].append((memories_h, memories_r, memories_t))
                    # print(ripple_set)
        return ripple_set

    def forward(self, interaction):
        users = interaction[0].cpu().numpy()
        memories_h, memories_r, memories_t = {}, {}, {}
        for hop in range(self.n_hop):
            memories_h[hop] = []
            memories_r[hop] = []
            memories_t[hop] = []
            # print(users)
            for user in users:
                # print(user)
                # print(self.ripple_set)
                # print(self.ripple_set[user])
                memories_h[hop].append(self.ripple_set[user][hop][0])
                memories_r[hop].append(self.ripple_set[user][hop][1])
                memories_t[hop].append(self.ripple_set[user][hop][2])
        # memories_h, memories_r, memories_t = self.ripple_set[user]
        item = interaction[1].to(self.device)
        self.item_embeddings = self.entity_embedding(item)
        self.h_emb_list = []
        self.r_emb_list = []
        self.t_emb_list = []
        for i in range(self.n_hop):
            # [batch size * n_memory]
            head_ent = torch.cat(memories_h[i], dim=0).to(self.device)
            # print(head_ent.is_cuda)
            relation = torch.cat(memories_r[i], dim=0).to(self.device)
            tail_ent = torch.cat(memories_t[i], dim=0).to(self.device)
            # self.logger.info("Hop {}, size {}".format(i, head_ent.size(), relation.size(), tail_ent.size()))

            # [batch size * n_memory, dim]
            self.h_emb_list.append(self.entity_embedding(head_ent))

            # [batch size * n_memory, dim * dim]
            self.r_emb_list.append(self.relation_embedding(relation))

            # [batch size * n_memory, dim]
            self.t_emb_list.append(self.entity_embedding(tail_ent))

        o_list = self._key_addressing()
        y = o_list[-1]
        for i in range(self.n_hop - 1):
            y = y + o_list[i]
        scores = torch.sum(self.item_embeddings * y, dim=1)
        return scores

    def _key_addressing(self):
        r"""Conduct reasoning for specific item and user ripple set

        Returns:
            o_list (dict -> torch.cuda.FloatTensor): list of torch.cuda.FloatTensor n_hop * [batch_size, embedding_size]
        """
        o_list = []
        for hop in range(self.n_hop):
            # [batch_size * n_memory, dim, 1]
            h_emb = self.h_emb_list[hop].unsqueeze(2)

            # [batch_size * n_memory, dim, dim]
            r_mat = self.r_emb_list[hop].view(-1, self.embedding_size, self.embedding_size)
            # [batch_size, n_memory, dim]
            Rh = torch.bmm(r_mat, h_emb).view(-1, self.n_memory, self.embedding_size)

            # [batch_size, dim, 1]
            v = self.item_embeddings.unsqueeze(2)

            # [batch_size, n_memory]
            probs = torch.bmm(Rh, v).squeeze(2)

            # [batch_size, n_memory]
            probs_normalized = self.softmax(probs)

            # [batch_size, n_memory, 1]
            probs_expanded = probs_normalized.unsqueeze(2)

            tail_emb = self.t_emb_list[hop].view(-1, self.n_memory, self.embedding_size)

            # [batch_size, dim]
            o = torch.sum(tail_emb * probs_expanded, dim=1)

            self.item_embeddings = self.transform_matrix(self.item_embeddings + o)
            # item embedding update
            o_list.append(o)
        return o_list

    def calculate_loss(self, interaction):
        label = interaction[2]
        output = self.forward(interaction)
        # print(label)
        # # print("output: "+type(output))
        # print(output)
        label=torch.FloatTensor(label.detach().cpu().numpy())
        output=torch.FloatTensor(output.detach().cpu().numpy())
        # print(label)
        # print(output)
        rec_loss = self.loss(output, label)
        kge_loss = None
        for hop in range(self.n_hop):
            # (batch_size * n_memory, 1, dim)
            h_expanded = self.h_emb_list[hop].unsqueeze(1)
            # (batch_size * n_memory, dim)
            t_expanded = self.t_emb_list[hop]
            # (batch_size * n_memory, dim, dim)
            r_mat = self.r_emb_list[hop].view(-1, self.embedding_size, self.embedding_size)
            # (N, 1, dim) (N, dim, dim) -> (N, 1, dim)
            hR = torch.bmm(h_expanded, r_mat).squeeze(1)
            # (N, dim) (N, dim)
            hRt = torch.sum(hR * t_expanded, dim=1)
            if kge_loss is None:
                kge_loss = torch.mean(self.sigmoid(hRt))
            else:
                kge_loss = kge_loss + torch.mean(self.sigmoid(hRt))

        reg_loss = None
        for hop in range(self.n_hop):
            tp_loss = self.l2_loss(self.h_emb_list[hop], self.t_emb_list[hop], self.r_emb_list[hop])
            if reg_loss is None:
                reg_loss = tp_loss
            else:
                reg_loss = reg_loss + tp_loss
        reg_loss = reg_loss + self.l2_loss(self.transform_matrix.weight)
        loss = rec_loss - self.kg_weight * kge_loss + self.reg_weight * reg_loss

        return loss

    def predict(self, interaction):
        scores = self.forward(interaction)
        return scores

    def _key_addressing_full(self):
        r"""Conduct reasoning for specific item and user ripple set

        Returns:
            o_list (dict -> torch.cuda.FloatTensor): list of torch.cuda.FloatTensor
                n_hop * [batch_size, n_item, embedding_size]
        """
        o_list = []
        for hop in range(self.n_hop):
            # [batch_size * n_memory, dim, 1]
            h_emb = self.h_emb_list[hop].unsqueeze(2)

            # [batch_size * n_memory, dim, dim]
            r_mat = self.r_emb_list[hop].view(-1, self.embedding_size, self.embedding_size)
            # [batch_size, n_memory, dim]
            Rh = torch.bmm(r_mat, h_emb).view(-1, self.n_memory, self.embedding_size)

            batch_size = Rh.size(0)

            if len(self.item_embeddings.size()) == 2:
                # [1, n_item, dim]
                self.item_embeddings = self.item_embeddings.unsqueeze(0)
                # [batch_size, n_item, dim]
                self.item_embeddings = self.item_embeddings.expand(batch_size, -1, -1)
                # [batch_size, dim, n_item]
                v = self.item_embeddings.transpose(1, 2)
                # [batch_size, dim, n_item]
                v = v.expand(batch_size, -1, -1)
            else:
                assert len(self.item_embeddings.size()) == 3
                # [batch_size, dim, n_item]
                v = self.item_embeddings.transpose(1, 2)

            # [batch_size, n_memory, n_item]
            probs = torch.bmm(Rh, v)

            # [batch_size, n_memory, n_item]
            probs_normalized = self.softmax(probs)

            # [batch_size, n_item, n_memory]
            probs_transposed = probs_normalized.transpose(1, 2)

            # [batch_size, n_memory, dim]
            tail_emb = self.t_emb_list[hop].view(-1, self.n_memory, self.embedding_size)

            # [batch_size, n_item, dim]
            o = torch.bmm(probs_transposed, tail_emb)

            # [batch_size, n_item, dim] [batch_size, n_item, dim] -> [batch_size, n_item, dim]
            self.item_embeddings = self.transform_matrix(self.item_embeddings + o)
            # item embedding update
            o_list.append(o)
        return o_list

    def full_sort_predict(self, interaction):
        users = interaction[0].cpu().numpy()
        memories_h, memories_r, memories_t = {}, {}, {}
        for hop in range(self.n_hop):
            memories_h[hop] = []
            memories_r[hop] = []
            memories_t[hop] = []
            for user in users:
                memories_h[hop].append(self.ripple_set[user][hop][0])
                memories_r[hop].append(self.ripple_set[user][hop][1])
                memories_t[hop].append(self.ripple_set[user][hop][2])
        # memories_h, memories_r, memories_t = self.ripple_set[user]
        # item = interaction[self.ITEM_ID]
        self.item_embeddings = self.entity_embedding.weight[:self.n_items]
        # self.item_embeddings = self.entity_embedding(item)

        self.h_emb_list = []
        self.r_emb_list = []
        self.t_emb_list = []
        for i in range(self.n_hop):
            # [batch size * n_memory]
            head_ent = torch.cat(memories_h[i], dim=0)
            relation = torch.cat(memories_r[i], dim=0)
            tail_ent = torch.cat(memories_t[i], dim=0)
            # self.logger.info("Hop {}, size {}".format(i, head_ent.size(), relation.size(), tail_ent.size()))

            # [batch size * n_memory, dim]
            self.h_emb_list.append(self.entity_embedding(head_ent))

            # [batch size * n_memory, dim * dim]
            self.r_emb_list.append(self.relation_embedding(relation))

            # [batch size * n_memory, dim]
            self.t_emb_list.append(self.entity_embedding(tail_ent))

        o_list = self._key_addressing_full()
        y = o_list[-1]
        for i in range(self.n_hop - 1):
            y = y + o_list[i]
        # [batch_size, n_item, dim] [batch_size, n_item, dim]
        scores = torch.sum(self.item_embeddings * y, dim=-1)
        return scores.view(-1)
