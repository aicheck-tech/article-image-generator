import argparse
import io
import logging
from PIL import Image

import datasets
import requests
import torch
from torch.utils.data import DataLoader

from article_image_generator.backend.clip_classification import ClipClassification
from article_image_generator.settings import BATCH_SIZE, DATASETS


logger = logging.getLogger(__name__)


def calculate_acc_loss_avg(corrects: int,
                           loss: float,
                           batch_num: int,
                           loss_fn,
                           prediction: torch.Tensor,
                           label: torch.Tensor
                           ):
    """ Calculates the accuracy and loss of the model,
        by averaging the loss and accuracy of the model"""
    new_loss = loss + loss_fn(prediction, label)
    new_corrects = corrects + ((1 / (batch_num + 1)) * (new_loss.item() - corrects))
    return new_corrects, new_loss


def calculate_acc_loss_press(corrects: int,
                             loss: float,
                             loss_fn,
                             prediction: torch.Tensor,
                             label: torch.Tensor
                             ):
    """ Calculates the accuracy and loss of the model,
        if model prediction is correct"""
    if torch.argmax(prediction) == label:
        corrects += 1
    new_loss = loss + loss_fn(prediction, label)
    return corrects, new_loss


def train(train_loader, loss_fn, optimizer, model) -> None:
    model.train()
    data_size = len(train_loader.dataset)
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
            logger.info(f"\tloss: {loss:>8f}, [{progress:>5f}/{data_size:>5f}]")


def evaluate_model(model, data_loader, loss_fn):
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
    # FIXME rename loss2
    logger.info(
        f"Results: TestError={(100 * correct):>0.1f}%, AvgLoss={loss:>8f}"
        f"MyAccuracy={(100 * correct2):>0.1f}%, AvgLoss2={loss2:>8f}"
    )
    return correct, loss, correct2, loss2


def load_dataset(dataset: str):
    """ Loads the dataset from the json file, and splits it into train and test data"""

    def collate_fn(data: list):
        titles = [doc['title'] for doc in data]
        texts = [doc['text'] for doc in data]
        image_urls = [doc['imgURL'] for doc in data]
        labels = [doc['label'] for doc in data]
        texts = [f"{title}\n{text}" for title, text in zip(titles, texts)]

        image_list = []
        for img_url in image_urls:
            try:
                response = requests.get(img_url)
                response.raise_for_status()
                image = Image.open(io.BytesIO(response.content))
                image_list.append(image)
            except requests.exceptions.RequestException:
                logger.exception(f"Downloading image failed for url {img_url}.")

        batch_text = [model.tokenize(text) for text in texts]
        batch_images = [model.convert_img(img) for img in image_list]
        batch_labels = torch.tensor(labels)
        return torch.concat(batch_text), torch.concat(batch_images), batch_labels

    train_data = datasets.load_dataset(DATASETS[dataset], split="train")
    test_data = datasets.load_dataset(DATASETS[dataset], split="test")

    train_dataloader = DataLoader(
        dataset=train_data,
        batch_size=BATCH_SIZE,
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

    evaluate_model(model, test_dataloader, loss_fn)
    evaluate_model(model, train_dataloader, loss_fn)


def start_test(model, train_dataloader: DataLoader, test_dataloader: DataLoader) -> None:
    loss_fn = torch.nn.CrossEntropyLoss()

    evaluate_model(model, test_dataloader, loss_fn)
    evaluate_model(model, train_dataloader, loss_fn)


if __name__ == "__main__":
    # CLI for fast training and testing and example testing
    def get_args():
        parser = argparse.ArgumentParser(description='Train.py Argument Parser')
        parser.add_argument('--path-to-model', type=str, help='Path to the model')
        parser.add_argument('--dataset', type=str, help='Dataset name')
        parser.add_argument('--output-path', type=str, help='Output path')
        parser.add_argument('--lr', type=float, help='Learning rate')
        parser.add_argument('--mode', choices=['train', 'test'],
                            help='Mode: "train" to train the model, "test" to test the model')
        return parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ClipClassification()
    train_dataloader, test_dataloader = load_dataset("bbc")
    output = "model.pth"
    learning_rate = 1e-4
    args = get_args()
    if args.path_to_model:
        try:
            model = model.load_state_dict(torch.load(args.path_to_model))
        except FileNotFoundError:
            logger.info("Model not found")
    if args.dataset:
        train_dataloader, test_dataloader = load_dataset(args.dataset)
    if args.output_path:
        output = args.output_path
    if args.lr:
        learning_rate = args.lr
    if args.mode == "train":
        start_train(model, train_dataloader,
                    test_dataloader, output, learning_rate)
    else:
        start_test(model, train_dataloader, test_dataloader)
