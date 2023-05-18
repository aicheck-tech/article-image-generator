import argparse
from PIL import Image
import io
import logging

import requests
import torch
from torch.utils.data import DataLoader

import anlys
from clip_classification import ClipClassification
import train_settings


def calculate_acc_loss_avg(corrects, loss, batch_num, lossFn, prediction, label):
    """ Calculates the accuracy and loss of the model,
        by averaging the loss and accuracy of the model"""
    loss += lossFn(prediction, label)
    corrects += ((1 / (batch_num + 1)) * (loss.item() - corrects))
    return corrects, loss


def calculate_acc_loss_press(corrects, loss, lossFn, prediction, label):
    """ Calculates the accuracy and loss of the model,
        if model prediction is correct"""
    if torch.argmax(prediction) == label:
        corrects += 1
    loss += lossFn(prediction, label)
    return corrects, loss


def train(train_loader, loss_fn, optimizer, model) -> None:
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
            progress = batch * len(labels)
            log = f"loss: {loss:>8f}, [{progress:>5f}/{data_size:>5f}]\n"
            logging.info(log)


def test(model, data_loader, loss_fn) -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data_size = len(data_loader.dataset)
    num_batches = len(data_loader)
    model.eval()
    """
    loss, correct are for the average loss and accuracy (Test Error)
    loss2, correct2 are for the accuracy of the model,
    if it predicts the correct label
    """
    loss, correct, loss2, correct2 = 0, 0, 0, 0
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
    loss /= num_batches
    loss2 /= num_batches
    correct /= data_size
    correct2 /= data_size
    log = f"Results: \n Test Error: {(100*correct):>0.1f}% \
            , Avg loss: {loss:>8f}\n \
            My Accuracy: {(100*correct2):>0.1f}% \
            , Avg loss: {loss2:>8f}\n"
    logging.info(log)
    return correct, loss, correct2, loss2


def load_dataset(dataset: str):
    """ Loads the dataset from the json file,
        and splits it into train and test data"""
    def collate_fn(data):
        titles, texts, images, labels = zip(
            *[(d['title'], d['text'], d['imgURL'], d['label']) for d in data])
        texts = [f"{title}\n{text}" for title, text in zip(titles, texts)]
        batch_text = [model.tokenize(text) for text in texts]
        images = [Image.open(io.BytesIO(requests.get(img).content))
                  for img in images]
        batch_images = [model.convert_img(img) for img in images]
        batch_labels = torch.tensor(labels)
        return torch.concat(batch_text), torch.concat(batch_images), batch_labels

    json_data = anlys.load_json_to_list(train_settings.DATASETS[dataset])

    train_data, test_data = anlys.split_data(
        json_data, train_settings.TRAIN_TEST_SPLIT_RATIO)

    train_dataloader = DataLoader(
        dataset=train_data,
        batch_size=train_settings.BATCH_SIZE,
        shuffle=True,
        collate_fn=collate_fn,
    )

    test_dataloader = DataLoader(
        dataset=test_data,
        batch_size=1,
        shuffle=True,
        collate_fn=collate_fn,
    )

    return train_dataloader, test_dataloader


def start_train(model,
                train_dataloader: DataLoader,
                test_dataloader: DataLoader,
                output_path: str, learning_rate: float) -> None:
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()

    train(train_dataloader, loss_fn, optimizer, model)
    torch.save(model.state_dict(), output_path)

    test(model, test_dataloader, loss_fn)
    test(model, train_dataloader, loss_fn)


def start_test(model, train_dataloader: DataLoader, test_dataloader: DataLoader) -> None:
    loss_fn = torch.nn.CrossEntropyLoss()

    test(model, test_dataloader, loss_fn)
    test(model, train_dataloader, loss_fn)


if __name__ == "__main__":
    # CLI for fast training and testing and example testing

    def get_args():
        parser = argparse.ArgumentParser(description='Train.py Argument Parser')
        parser.add_argument('--path-to-model', type=str, help='Path to the model')
        parser.add_argument('--dataset', type=str, help='Dataset name')
        parser.add_argument('--output-path', type=str, help='Output path')
        parser.add_argument('--lr', type=float, help='Learning rate')
        return parser.parse_args()

    model = ClipClassification()
    train_dataloader, test_dataloader = load_dataset("bbc")
    output = "model.pth"
    learning_rate = 1e-3
    args = get_args()
    if args.path_to_model:
        model = model.load_state_dict(torch.load(args.path_to_model))
    if args.dataset:
        train_dataloader, test_dataloader = load_dataset(args.dataset)
    if args.output:
        output = args.output
    if args.learning_rate:
        learning_rate = args.learning_rate
    if len(args) > 1:
        if args[1] == "train":
            start_train(model, train_dataloader,
                        test_dataloader, output, learning_rate)
        elif args[1] == "test":
            start_test(model, train_dataloader, test_dataloader)
    else:
        start_test(model, train_dataloader, test_dataloader)
