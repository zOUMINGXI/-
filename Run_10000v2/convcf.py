# -*- coding: utf-8 -*-
# @Time   : 2020/10/6
# @Author : Yingqian Min
# @Email  : eliver_min@foxmail.com

r"""
ConvNCF
################################################
Reference:
    Xiangnan He et al. "Outer Product-based Neural Collaborative Filtering." in IJCAI 2018.

Reference code:
    https://github.com/duxy-me/ConvNCF
"""

import torch
import torch.nn as nn
from recbole.model.layers import MLPLayers, CNNLayers
from recbole.model.loss import BPRLoss

class ConvNCFBPRLoss(nn.Module):
    """ ConvNCFBPRLoss, based on Bayesian Personalized Ranking,

    Shape:
        - Pos_score: (N)
        - Neg_score: (N), same shape as the Pos_score
        - Output: scalar.

    Examples::

        >>> loss = ConvNCFBPRLoss()
        >>> pos_score = torch.randn(3, requires_grad=True)
        >>> neg_score = torch.randn(3, requires_grad=True)
        >>> output = loss(pos_score, neg_score)
        >>> output.backward()
    """

    def __init__(self):
        super(ConvNCFBPRLoss, self).__init__()

    def forward(self, pos_score, neg_score):
        distance = pos_score - neg_score
        # print(distance)
        loss = torch.sum(torch.log((1 + torch.exp(-distance))))
        return loss


class ConvNCF(nn.Module):
    r"""ConvNCF is a a new neural network framework for collaborative filtering based on NCF.
    It uses an outer product operation above the embedding layer,
    which results in a semantic-rich interaction map that encodes pairwise correlations between embedding dimensions.
    We carefully design the data interface and use sparse tensor to train and test efficiently.
    We implement the model following the original author with a pairwise training mode.
    """

    def __init__(self, dataset):
        super(ConvNCF, self).__init__()

        # load dataset info

        # load parameters info
        self.device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.embedding_size = 64
        self.cnn_channels = [1, 32, 32, 32, 32]
        self.cnn_kernels = [4, 4, 2, 2]
        self.cnn_strides = [4, 4, 2, 2]
        self.dropout_prob = 0.2
        self.regs = [0.1, 0.1]
        self.n_users=dataset.user_num
        self.n_items=dataset.course_num
        # define layers and loss
        self.user_embedding = nn.Embedding(self.n_users+12000, self.embedding_size).to(self.device)
        self.item_embedding = nn.Embedding(self.n_items+12000, self.embedding_size).to(self.device)
        self.cnn_layers = CNNLayers(self.cnn_channels, self.cnn_kernels, self.cnn_strides, activation='relu').to(self.device)
        self.predict_layers = MLPLayers([self.cnn_channels[-1], 1], self.dropout_prob, activation='none').to(self.device)
        self.loss = BPRLoss()
        self.lr=0.005
    def forward(self, user, item):
        user_e = self.user_embedding(user)
        item_e = self.item_embedding(item)

        interaction_map = torch.bmm(user_e.unsqueeze(2), item_e.unsqueeze(1)).to(self.device)
        interaction_map = interaction_map.unsqueeze(1)

        cnn_output = self.cnn_layers(interaction_map)
        cnn_output = cnn_output.sum(axis=(2, 3))

        prediction = self.predict_layers(cnn_output)
        prediction = prediction.squeeze(-1)

        return prediction

    def reg_loss(self):
        r"""Calculate the L2 normalization loss of model parameters.
        Including embedding matrices and weight matrices of model.

        Returns:
            loss(torch.FloatTensor): The L2 Loss tensor. shape of [1,]
        """
        reg_1, reg_2 = self.regs[:2]
        loss_1 = reg_1 * self.user_embedding.weight.norm(2)
        loss_2 = reg_1 * self.item_embedding.weight.norm(2)
        loss_3 = 0
        for name, parm in self.cnn_layers.named_parameters():
            if name.endswith('weight'):
                loss_3 = loss_3 + reg_2 * parm.norm(2)
        for name, parm in self.predict_layers.named_parameters():
            if name.endswith('weight'):
                loss_3 = loss_3 + reg_2 * parm.norm(2)
        return loss_1 + loss_2 + loss_3

    def calculate_loss(self, interaction):
        pos_index = []
        neg_index=[]
        for i in range(len(interaction[0])):
            if interaction[2][i] == 1:
                pos_index.append(i)
            else:
                neg_index.append(i)
        neg_item = interaction[1][neg_index]
        pos_item = interaction[1][pos_index]
        pos_user=interaction[0][pos_index]
        neg_user = interaction[0][neg_index]
        pos_item_score= self.forward(pos_user, pos_item)
        neg_item_score=self.forward(neg_user,neg_item)
        a = len(pos_item_score)
        b = len(neg_item_score)
        pos_item_score = pos_item_score[:min(a, b) - 1]
        neg_item_score = neg_item_score[:min(a, b) - 1]
        # print(pos_item_score.shape)
        # print(neg_item_score.shape)
        loss = self.loss(pos_item_score, neg_item_score)
        opt_loss = loss + self.reg_loss()

        return opt_loss

    def predict(self, interaction):
        user = interaction[0]
        item = interaction[1]
        return self.forward(user, item)
