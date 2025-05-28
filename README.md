# 📘 All Pairs Matching with PySpark

This project solves the **All Pairs Matching Problem** using two approaches: **naive pairs** and **group pairs matching**. Implemented in **Python** using **PySpark**, the system follows the **Map-Reduce model** to compute **Jaccard similarity** between users based on the movies they have rated.

The application runs inside a Dockerized Spark cluster, allowing controlled benchmarking across datasets of different sizes.

---

## 📄 Description

- What problem does this project solve?
- What approaches are implemented?
- What technologies are used?

---

## 📂 Project Structure

    ├── docker-compose.yml # Defines the Spark cluster (1 master, 2 workers)
    ├── .env # Environment variables (mode and dataset size)
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
  git clone https://github.com/your-username/all-pairs-matching.git
  cd all-pairs-matching
```

### 2. Configure Environment (edit .env file)

### 3.Run the Application
```bash
  docker-compose up --build
```

## 🧠 Problem Overview
Explain the All Pairs Matching Problem and how Jaccard similarity is used.

### 🛠️ Approaches

### 1. 🔹 Naive Matching
Description
### 2. 🔹 Group-Based Matching
Description

## 🧪 Input & Output

## 🐳 Dockerized Spark Cluster

## ⏱️ Performance Benchmarking

## 📦 Requirements

## 📄 License

## 👤 Author

