from pathlib import Path

def get_dataset_path(filename):
    """Returns absolute path to dataset file"""
    return Path(__file__).parent.parent / "datasets" / filename