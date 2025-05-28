# 📘 All Pairs Matching with PySpark

This project solves the **All Pairs Matching Problem** using two approaches: **naive pairs** and **group pairs matching**. Implemented in **Python** using **PySpark**, the system follows the **Map-Reduce model** to compute **Jaccard similarity** between users based on the movies they have rated.

The application runs inside a Dockerized Spark cluster, allowing controlled benchmarking across datasets of different sizes.

---

## 📂 Project Structure

    ├── docker-compose.yml # Defines the Spark cluster structure (1 master, 2 workers)
    ├── .env # Environmental variables (approach and dataset size)
    ├── datasets/
    │ └── movies-ratings.csv # Movie ratings dataset
    ├── spark/
    │ ├── Dockerfile # Docker setup for Spark nodes
    │ └── spark-env.sh # Spark environment variables
    └── src/
    ├── main.py # Entrypoint that loads the selected matching mode
    ├── naive_runner.py # Naive matching implementation
    ├── group_runner.py # Group-based matching implementation
    ├── Dockerfile # Docker setup for the PySpark app
    └── requirements.txt # Python dependencies (e.g., pyspark)

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
  git clone https://github.com/alexandrosadam/DWS-All-pairs-matching-problem.git
  cd DWS-All-pairs-matching-problem
```

### 2. Configure Environment (edit .env file)

#### Specify the matching mode: either 'naive' or 'group'
MODE=group

#### Choose dataset size: small, medium, or large
DATASET_SIZE=large

### 3.Run the Application
Inside the project's root folder execute:
```bash
  docker-compose up --build
```

## 🧠 Problem Overview
The All Pairs Matching Problem involves identifying similar entities by comparing all possible pairs in a dataset. In this project, each entity is a user, and similarity is based on the set of movies each user has rated. The project uses Jaccard Similarity to quantify similarity between users. The Jaccard index is calculated as: J(A, B) = |A ∩ B| / |A ∪ B|


### 🛠️ Approaches

### 1. 🔹 Naive Matching
This approach generates all possible user pairs from the dataset and computes their Jaccard similarity. Although straightforward, it results in a computational complexity of O(n²), making it less efficient for large datasets.

### 2. 🔹 Group-Based Matching
To reduce computational load, this method first groups users into batches (e.g., 50 users per group), and computes similarities only within each group. This reduces the total number of comparisons and is better suited for scaling on larger datasets.

## 🧪 Input & Output
Input: A CSV file located in datasets/ directory named movies-ratings.csv. Each record includes at least userId and movieId columns.

Output:A CSV file containing tuples in the format (user1, user2, similarity_score).
The file is saved in the output path within the running container depending on the selected approach:

- naive_user_similarities.csv

- group_user_similarities.csv

## 🐳 Dockerized Spark Cluster
The application runs inside a Dockerized Spark Cluster, configured using docker-compose. The cluster consists of:

- 1 Spark Master

- 2 Spark Workers

Resource configurations (CPU, memory) can be adjusted per worker. Environment variables are set via a .env file to define processing mode (MODE=naive or MODE=group) and dataset size (DATASET_SIZE=small, medium, or large).

## ⏱️ Performance Benchmarking
Benchmarking was performed on two cluster configurations:

2 cores, 2 GB RAM per worker

4 cores, 4 GB RAM per worker

| Approach    | Dataset Size | Time (2C/2G) | Time (4C/4G) |
| ----------- | ------------ | ------------ | ------------ |
| Naive       | small        | 15.28 sec    | 15.90 sec    |
|             | medium       | 44.70 sec    | 44.50 sec    |
|             | large        | 143.40 sec   | 140.00 sec   |
| Group-Based | small        | 10.00 sec    | 9.50 sec     |
|             | medium       | 11.00 sec    | 11.25 sec    |
|             | large        | 12.85 sec    | 15.00 sec    |


## 📦 Requirements
The Python dependencies are listed in requirements.txt. They are automatically installed in the Docker container.

Key dependencies:
- pyspark

## 📄 License
This project is licensed under the MIT License

## 👤 Author
Alexander Adam

