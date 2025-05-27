from pathlib import Path

from pyspark import SparkFiles
from pyspark.sql import SparkSession
from utils import get_dataset_path, save_similarities, calculate_user_similarity, get_dataset_size_limit
from pyspark.rdd import RDD
from typing import Dict, Set, Tuple


class NaiveRunner:
    @classmethod
    def execute_naive_all_pairs_matching(cls, dataset_size: str):
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

            """
                In the below pipeline:
                1) Converts DataFrame to RDD (Resilient Distributed Dataset)
                2) Mapping phase: generate key-value pairs in format (user, {movie})
                3) Reduce phase: Merge sets for same user
                4) Driver collection: create a map for each user in format {user1: {movie1, movie2,...}, ...}
            """
            user_movies: Dict[str, Set[str]] = movies_ratings_data.rdd \
                .map(lambda row: (row['userId'], {row['movieId']})) \
                .reduceByKey(lambda a, b: a | b) \
                .collectAsMap()

            # Generate all unique user pairs
            user_ids = list(user_movies.keys())
            user_pairs = []

            for i in user_ids:
                for j in user_ids:
                    if i < j:
                        user_pairs.append((i, j))

            # Broadcast data to workers and Map phase 2 to calculate the similarities among users ratings
            broadcast_user_movies = spark.sparkContext.broadcast(user_movies)

            similarities: RDD[Tuple[str, str, float]] = spark.sparkContext.parallelize(user_pairs) \
                .map(lambda pair: calculate_user_similarity(pair, broadcast_user_movies))

            # Save results: (user1, user2, similarity_score) into a csv file
            save_similarities(similarities, "naive_user_similarities")

        finally:
            spark.stop()
