from pymilvus import connections, db, MilvusClient, DataType


class MilvusHelper:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.connect()

    def create_db(self):
        conn = connections.connect(host=self.host, port=self.port)
        database = db.create_database(self.db_name)
        pass

    def connect(self):
        cluster_endpoint = f"http://{self.host}:{self.port}"
        # 1. Set up a Milvus client
        client = MilvusClient(
            uri=cluster_endpoint,
            db_name=self.db_name,
        )
        self.client = client

    def describe_collection(self, collection_name):
        # 5. View Collections
        res = self.client.describe_collection(
            collection_name=collection_name
        )
        print(res)

    def drop_collection_index(self, collection_name, index_name):
        res = self.client.drop_index(
            collection_name=collection_name,
            index_name=index_name
        )
        print(res)

    def describe_collection_index(self, collection_name, index_name):
        res = self.client.describe_index(
            collection_name=collection_name,
            index_name=index_name
        )
        print(res)

    def list_collection_indexes(self, collection_name):
        res = self.client.list_indexes(
            collection_name=collection_name
        )
        print(res)

    def drop_collection(self, collection_name):
        self.client.drop_collection(
            collection_name=collection_name
        )

    def load_collection(self, collection_name):
        self.client.load_collection(
            collection_name=collection_name
        )
        res = self.client.get_load_state(
            collection_name=collection_name
        )
        print(res)

    def release_collection(self, collection_name):
        self.client.release_collection(
            collection_name=collection_name
        )
        res = self.client.get_load_state(
            collection_name=collection_name
        )
        print(res)

    def list_all_collection(self):
        res = self.client.list_collections()
        print(res)

    def create_partition(self, collection_name, partition_name):
        self.client.create_partition(
            collection_name=collection_name,
            partition_name=partition_name
        )

    def drop_partition(self, collection_name, partition_name):
        self.client.drop_partition(
            collection_name=collection_name,
            partition_name=partition_name
        )

    def load_partition(self, collection_name, partition_name):
        self.client.load_partitions(
            collection_name=collection_name,
            partition_name=partition_name
        )

    def list_partitions(self, collection_name):
        res = self.client.list_partitions(collection_name=collection_name)
        print(res)

    def has_partitions(self, collection_name) -> bool:
        res = self.client.has_partition(collection_name=collection_name)
        return res

    def insert(self, collection_name, data):
        self.client.insert(collection_name=collection_name, data=data)
