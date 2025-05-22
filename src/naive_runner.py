import os

from pyspark.sql import SparkSession
from utils import get_dataset_path, get_project_root_path, save_similarities


class NaiveRunner:
    @classmethod
    def execute_naive_all_pairs_matching(cls):
        output_path: str = os.path.join(get_project_root_path(), "naive_user_similarities")
        spark = SparkSession.builder.appName("NaiveAllPairsMatching").getOrCreate()

        # Load the movie ratings data
        movies_ratings_data = spark.read.csv(str(get_dataset_path()), header=True)

        # Data processing step, converts DataFrame to RDD (Resilient Distributed Dataset)
        # The below pipeline does 1) create (user, {movie}) 2) Merge sets for same user 3) {user1: {movie1, movie2,...}, ...}
        user_movies = movies_ratings_data.rdd \
        .map(lambda row: (row['userId'], { row['movieId']})) \
        .reduceByKey(lambda a, b: a | b) \
        .collectAsMap()

        # Generate all unique user pairs
        user_ids = list(user_movies.keys())
        user_pairs = []

        for i in user_ids:
            for j in user_ids:
                if i < j:
                    user_pairs.append((i, j))

        # Broadcast data to workers
        broadcast_user_movies = spark.sparkContext.broadcast(user_movies)

        # Calculate user-user similarities
        def calculate_user_similarity(pair):
            user1, user2 = pair
            movies1 = broadcast_user_movies.value[user1]
            movies2 = broadcast_user_movies.value[user2]
            intersection = len(movies1 & movies2)
            union = len(movies1 | movies2)
            return user1, user2, intersection / union if union != 0 else 0

        similarities = spark.sparkContext.parallelize(user_pairs).map(calculate_user_similarity)

        # Save results: (user1, user2, similarity_score)
        # Converting RDD to DataFrame with named columns
        save_similarities(similarities)

        spark.stop()
