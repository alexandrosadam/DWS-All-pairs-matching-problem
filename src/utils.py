import os
import glob
import shutil

from typing import Dict, Set, Tuple, List, Hashable
from pathlib import Path

from pyspark import Broadcast


def get_project_root_path():
    """Returns the project root path"""
    return Path(__file__).parent.parent

def get_dataset_path():
    """Returns absolute path to dataset file"""
    return get_project_root_path() / "datasets" / "movies-ratings.csv"


def calculate_user_similarity(pair: Tuple[str, str], broadcast_user_movies: Broadcast[dict[Hashable, set]] ) ->  Tuple[str, str, float]:
    """
    Calculates Jaccard similarity between two users based on rated movies.

    Args:
        pair: Tuple of (user1_id, user2_id)
        broadcast_user_movies: Broadcast a dictionary of {user_id: set_of_movie_ids}

    Returns:
        Tuple of (user1_id, user2_id, similarity_score)
    """
    user1, user2 = pair
    movies1 = broadcast_user_movies.value[user1]
    movies2 = broadcast_user_movies.value[user2]

    intersection = len(movies1 & movies2)
    union = len(movies1 | movies2)

    return user1, user2, intersection / union if union != 0 else 0


def save_similarities(similarities):
    # Configure paths
    temp_path = os.path.join(get_project_root_path(), "temp__naive_similarities")
    final_path = os.path.join(get_project_root_path() / "output", "naive_user_similarities.csv")

    # Write to temp location
    (similarities.toDF(["user1", "user2", "similarity"])
     .coalesce(1)
     .write.csv(temp_path, mode="overwrite", header=True))

    # Rename the output file
    part_files = glob.glob(os.path.join(temp_path, "part-*.csv"))
    shutil.move(part_files[0], final_path)
    shutil.rmtree(temp_path)
