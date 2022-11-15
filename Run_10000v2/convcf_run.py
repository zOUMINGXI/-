import torch.optim
from torch.utils.data import DataLoader
from convcf import ConvNCF
from dataset_newone import MyDataset_test
from dataset_oldone import  MyDataset_train
import eval_rec
def train_epochs(model,train_dataloader):
    model.train()
    optimizer=torch.optim.Adam(model.parameters(),lr=model.lr)
    train_loss=0
    loss_func=model.calculate_loss
    n=0
    for interaction in train_dataloader:
        # print(interaction)
        interaction[0]=torch.as_tensor(interaction[0])
        interaction=[data.to(model.device) for data in interaction]
        optimizer.zero_grad()
        loss=loss_func(interaction)
        train_loss+=loss.item()
        loss.backward()
        optimizer.step()
        n+=interaction[0].shape[0]
    return train_loss/n


def test_epochs(model,test_dataloder):
    device11 = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.eval()
    test_loss = 0
    loss_func = model.calculate_loss
    n = 0
    num=0
    scores = torch.ones(1).to(device11)
    with torch.no_grad():
        for interaction in test_dataloder:
            # num+=1
            # if num==2500:
            #     break
            interaction = [data.to(model.device) for data in interaction]
            loss = loss_func(interaction)
            test_loss += loss.item()
            n += interaction[0].shape[0]
            scores = torch.cat((scores, model.predict(interaction).to(model.device)), 0)
    scores = scores[1:]
    # print(len(scores))120
    # print(len(test_data))3
    hr5, hr10, ndcg5, ndcg10, maps, mrrs = eval_rec.eval_rating(scores,test_data=test_data)
    hr5, hr10, ndcg5, ndcg10, maps, mrrs = round(hr5, 4), round(hr10, 4), round(ndcg5, 4), round(ndcg10, 4), round(maps, 4), round(mrrs, 4)

    return test_loss / n, hr5, hr10, ndcg5, ndcg10, maps, mrrs
def train_test(model,epochs,train_dataloader,test_dataloader):
    for e,epoch in enumerate(range(epochs)):
        train_loss=train_epochs(model,train_dataloader)
        test_loss, hr5, hr10, ndcg5, ndcg10, maps, mrrs = test_epochs(model, test_dataloader)
        # print(epoch)
        print('Epoch: {}, Train loss: {}, Test loss: {}, hr2: {}, hr5: {}, ndcg2: {}, ndcg5: {}, maps: {}, mrrs: {}'.format(epoch, train_loss, test_loss, hr5, hr10, ndcg5, ndcg10, maps, mrrs))


if __name__=='__main__':
    print('begin')
    train_dataset=MyDataset_train()
    print('train_dataaset generation Done')
    train_dataloader=DataLoader(train_dataset,batch_size=100,shuffle=True)

    print('train_dataloader generation Done')
    net=ConvNCF(train_dataloader.dataset)
    print('net Done')
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    test_dataset=MyDataset_test()

    print('test_dataaset generation Done')
    test_dataloader=DataLoader(test_dataset,batch_size=100,shuffle=False)
    # for step,interaction in enumerate(train_dataloader):
    #     print(interaction)
    print('test_dataloader generation Done')
    test_data=test_dataset.get_test_set()
    train_test(net,10,train_dataloader,test_dataloader)
    print('train_and_test Done')
    print('Done!')



