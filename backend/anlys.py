import json

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