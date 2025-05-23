from pyspark.sql import SparkSession
from utils import get_dataset_path, save_similarities, calculate_user_similarity
from pyspark.rdd import RDD
from typing import Dict, Set, Tuple


class NaiveRunner:
    @classmethod
    def execute_naive_all_pairs_matching(cls):
        spark: SparkSession = SparkSession.builder.appName("NaiveAllPairsMatching").getOrCreate()

        try:
            # Spark driver reads the csv file and outputs a distributed DataFrame across worker nodes
            movies_ratings_data = spark.read.csv(str(get_dataset_path()), header=True)

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
