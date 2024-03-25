from datasets import load_dataset
import pandas as pd
from sentence_transformers import SentenceTransformer

# https://huggingface.co/thenlper/gte-large
embedding_model = SentenceTransformer("thenlper/gte-large")


def get_embedding(text: str) -> list[float]:
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []

    embedding = embedding_model.encode(text)

    return embedding.tolist()


def print_hi(name):
    # https://huggingface.co/datasets/AIatMongoDB/embedded_movies
    dataset = load_dataset("ComponentSoft/k8s-kubectl")

    # Convert the dataset to a pandas dataframe
    dataset_df = pd.DataFrame(dataset["train"])

    dataset_df = dataset_df.dropna(subset=["command"])
    print("\nNumber of missing values in each column after removal:")
    print(dataset_df.isnull().sum())

    dataset_df = dataset_df.drop(columns=["chain_of_thought"])
    # print(dataset_df.head(5))

    dataset_df = dataset_df.head(5)
    dataset_df["strs"] = dataset_df["question"] + ";" + dataset_df["description"]
    dataset_df["embedding"] = dataset_df["strs"].apply(get_embedding)
    print(dataset_df)


if __name__ == '__main__':
    print_hi('PyCharm')
