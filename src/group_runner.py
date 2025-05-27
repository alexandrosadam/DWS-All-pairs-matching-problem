import os

from pyspark import SparkFiles
from pyspark.sql import SparkSession
from utils import get_dataset_path, calculate_group_similarity, save_similarities, get_dataset_size_limit
from pyspark.rdd import RDD
from typing import List, Set, Tuple


class GroupRunner:
    @classmethod
    def execute_group_all_pairs_matching(cls, dataset_size: str, group_size: int = 50):
        spark: SparkSession = SparkSession.builder \
            .master("local[*]") \
            .appName("GroupAllPairsMatching") \
            .getOrCreate()

        try:
            # Spark driver reads the csv file and outputs a distributed DataFrame across worker nodes
            spark.sparkContext.addFile(str(get_dataset_path()))
            movies_ratings_data = spark.read.csv(f"file://{SparkFiles.get("movies-ratings.csv")}", header=True).limit(
                get_dataset_size_limit(dataset_size))

            movies_ratings_data = movies_ratings_data.repartition(4)

            # Convert data to RDD, generate key - value pairs and merge sets (like in naive approach)
            user_movies: RDD[Tuple[str, Set[str]]] = movies_ratings_data.rdd \
                .map(lambda row: (row['userId'], {row['movieId']})) \
                .reduceByKey(lambda a, b: a | b)

            # Group users into batches
            grouped_users: RDD[List[Tuple[str, Set[str]]]] = user_movies \
                .zipWithIndex() \
                .map(lambda x: (x[1] // group_size, x[0])) \
                .groupByKey() \
                .map(lambda x: list(x[1]))

            # Compute intra-group similarities
            similarities: RDD[Tuple[str, str, float]] = grouped_users.flatMap(calculate_group_similarity)

            # Save results: (user1, user2, similarity_score) into a csv file
            save_similarities(similarities, "group_user_similarities")

        finally:
            spark.stop()
