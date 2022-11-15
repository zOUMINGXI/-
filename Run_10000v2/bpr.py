import torch
import torch.nn as nn
from recbole.model.init import xavier_normal_initialization
from recbole.model.loss import BPRLoss
class BPR(nn.Module):
    def __init__(self,dataset):
        super(BPR, self).__init__()
        self.n_users=dataset.user_num
        self.n_items=dataset.course_num
        # load parameters info
        self.embedding_size = 64
        self.lr = 0.0012
        # define layers and loss
        self.device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.user_embedding = nn.Embedding(self.n_users+12000, self.embedding_size).to(self.device)
        self.item_embedding = nn.Embedding(self.n_items+12000, self.embedding_size).to(self.device)
        self.loss = BPRLoss()
        self.device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # parameters initialization
        self.apply(xavier_normal_initialization)

    def get_user_embedding(self, user):
        r""" Get a batch of user embedding tensor according to input user's id.

        Args:
            user (torch.LongTensor): The input tensor that contains user's id, shape: [batch_size, ]

        Returns:
            torch.FloatTensor: The embedding tensor of a batch of user, shape: [batch_size, embedding_size]
        """
        return self.user_embedding(user)

    def get_item_embedding(self, item):
        r""" Get a batch of item embedding tensor according to input item's id.

        Args:
            item (torch.LongTensor): The input tensor that contains item's id, shape: [batch_size, ]

        Returns:
            torch.FloatTensor: The embedding tensor of a batch of item, shape: [batch_size, embedding_size]
        """
        return self.item_embedding(item)

    def forward(self, user, item):
        user_e = self.get_user_embedding(user)
        # print(user_e.shape)
        item_e = self.get_item_embedding(item)
        # print(item_e.shape)
        return user_e, item_e

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
        # print(len(neg_item))
        # print(len(pos_item))
        pos_user_e, pos_e = self.forward(pos_user, pos_item)
        neg_user_e,neg_e=self.forward(neg_user,neg_item)
        #也不行，跟数据大小没关系？
        pos_item_score,neg_item_score = torch.mul(pos_user_e, pos_e).sum(dim=1),torch.mul(neg_user_e, neg_e).sum(dim=1)
        # print(pos_item_score,neg_item_score)
        a=len(pos_item_score)
        b=len(neg_item_score)
        pos_item_score=pos_item_score[:min(a,b)-1]
        neg_item_score=neg_item_score[:min(a,b)-1]
        loss = self.loss(pos_item_score, neg_item_score)
        return loss

    def predict(self, interaction):
        user = interaction[0]
        item = interaction[1]
        user_e, item_e = self.forward(user, item)
        return torch.mul(user_e, item_e).sum(dim=1)

    def full_sort_predict(self, interaction):
        user = interaction[0]
        user_e = self.get_user_embedding(user)
        all_item_e = self.item_embedding.weight
        score = torch.matmul(user_e, all_item_e.transpose(0, 1))
        return score.view(-1)
