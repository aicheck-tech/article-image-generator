import json


def load_jsonl_to_list(path):
    file = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            file.append(json.loads(line))
    return file


def save_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)


def load_json(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data


def load_json_to_list(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return list(data.values())


def split_data(data, ratio):
    train_data = []
    test_data = []
    for i in range(len(data)):
        if i < len(data) * ratio:
            train_data.append(data[i])
        else:
            test_data.append(data[i])
    return train_data, test_data