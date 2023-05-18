import json
from PIL import Image
from requests import get
import io
import torch
from torch.utils.data import DataLoader

from Clip_Classification import Clip_classification


def load(path):
    file = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            file.append(json.loads(line))
    return file


def split_data(data, ratio):
    train_data = []
    test_data = []
    for i in range(len(data)):
        if i < len(data) * ratio:
            train_data.append(data[i])
        else:
            test_data.append(data[i])
    return train_data, test_data

clip = Clip_classification()
optimizer = torch.optim.Adam(clip.parameters(), lr=1e-4)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1, gamma=0.9)
loss_fn = torch.nn.CrossEntropyLoss()

json_data = load("backend/data/BBC_dataset.jsonl")

train_data, test_data = split_data(json_data, 0.9)

def collate_fn(data):
    titles, texts, images, labels = zip(*[(d['title'], d['text'], d['imgURL'], d['label']) for d in data])
    batch_text = torch.concat([clip.tokenize(f"{title}\n{text}") for title, text in zip(titles, texts)])
    batch_images = torch.concat([clip.convert_img(Image.open(io.BytesIO(get(img).content))) for img in images])
    batch_labels = torch.tensor(labels)
    return batch_text, batch_images, batch_labels


train_dataloader = DataLoader(
    dataset=train_data,
    batch_size=1,
    shuffle=True,
    collate_fn=collate_fn,
)

test_dataloader = DataLoader(
    dataset=test_data,
    batch_size=1,
    shuffle=True,
    collate_fn=collate_fn,
)


def calculate_acc_loss_avg(corrects, loss, batch_num, lossFn, prediction, label):
    loss += lossFn(prediction, label)
    corrects += ((1 / (batch_num + 1)) * (loss.item() - corrects))
    return corrects, loss


def calculate_acc_loss_press(corrects, loss, lossFn, prediction, label):
    # Have to be used with batch size 1
    if torch.argmax(prediction) == label:
        corrects += 1
    loss += lossFn(prediction, label)
    return corrects, loss


def train(train_loader, loss_fn, optimizer, scheduler, model) -> None:
  model.train()
  data_size = len(train_loader.dataset)
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  for batch, (texts, images, labels) in enumerate(train_loader):
    texts = texts.to(device)
    images = images.to(device)
    labels = labels.to(device)
    prediction = model(texts, images)
    loss = loss_fn(prediction, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if batch % 100 == 0:
        loss, progress = loss, batch * len(labels)
        log = f"loss: {loss:>8f}, [{progress:>5f}/{data_size:>5f}]\n"
        scheduler.step()
        print(log)


def test(model, data_loader, loss_fn) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataSize = len(data_loader.dataset)
    numBatches = len(data_loader)
    model.eval()
    # loss, correct are for the average loss and accuracy (Test Error)
    # loss2, correct2 are for the accuracy of the model when it predicts the correct label
    loss, correct, loss2, correct2  = 0, 0, 0, 0
    with torch.no_grad():
        for batch, (texts, images, labels) in enumerate(data_loader):
            texts = texts.to(device)
            images = images.to(device)
            labels = labels.to(device)
            prediction = model(texts, images)
            loss = loss_fn(prediction, labels)

            correct, loss = calculate_acc_loss_avg(
                correct, loss, batch, loss_fn, prediction, labels)
            correct2, loss2 = calculate_acc_loss_press(
                correct2, loss2, loss_fn, prediction, labels)
    loss /= numBatches
    loss2 /= numBatches
    correct /= dataSize
    correct2 /= dataSize
    log = f"Results: \n Test Error: {(100*correct):>0.1f}%, Avg loss: {loss:>8f} \n My Accuracy: {(100*correct2):>0.1f}%, Avg loss: {loss2:>8f}\n"
    print(log)
    return correct, loss, correct2, loss2


test(clip, test_dataloader, loss_fn)
test(clip, train_dataloader, loss_fn)


train(train_dataloader, loss_fn, optimizer, scheduler, clip)
torch.save(clip.state_dict(), "clip.pth")

test(clip, test_dataloader, loss_fn)
test(clip, train_dataloader, loss_fn)
