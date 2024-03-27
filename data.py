import pandas as pd
from datasets import load_dataset


def get_data_sets(name):
    # https://huggingface.co/datasets/AIatMongoDB/embedded_movies
    dataset = load_dataset("ComponentSoft/k8s-kubectl")

    # Convert the dataset to a pandas dataframe
    dataset_df = pd.DataFrame(dataset["train"])

    dataset_df = dataset_df.dropna(subset=["command"])
    print("\nNumber of missing values in each column after removal:")
    print(dataset_df.isnull().sum())

    dataset_df = dataset_df.drop(columns=["chain_of_thought"])
    # print(dataset_df.head(5))

    # dataset_df = dataset_df.head(5)

    # 需要计算向量的字段
    dataset_df["strs"] = dataset_df["question"] + ";" + dataset_df["description"]

    print(dataset_df.columns)
    return dataset_df.to_dict("records")
