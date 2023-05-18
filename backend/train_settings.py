from pathlib import Path

TRAIN_TEST_SPLIT_RATIO = 0.9
BATCH_SIZE = 1

DATASETS = {
    "bbc": Path(__file__).parent / "data" / "bbc_dataset_v1.json"
}
