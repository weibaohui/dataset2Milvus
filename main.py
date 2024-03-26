from peewee import chunked
from pymilvus import MilvusClient, DataType

import SqliteDataBase
import Transformer
import data
from milvus_helper import MilvusHelper


def create_collection(client: MilvusClient, collection_name: str):
    # 3.1. Create schema
    schema = client.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )

    # 3.2. Add fields to schema
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
    schema.add_field(field_name="objective", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    schema.add_field(field_name="command_name", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    schema.add_field(field_name="command", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    schema.add_field(field_name="description", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    schema.add_field(field_name="syntax", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    schema.add_field(field_name="flags", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    schema.add_field(field_name="question", datatype=DataType.VARCHAR, max_length=1000, is_nullable=True)
    # 3.3. Prepare index parameters
    index_params = client.prepare_index_params()

    # 3.4. Add indexes
    index_params.add_index(
        field_name="vector",
        index_type="IVF_FLAT",
        metric_type="IP",  # COSINE 、 L2 或 IP
        params={"nlist": 128}
    )

    # 3.5. Create a collection with the index loaded simultaneously
    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params
    )
    pass


if __name__ == '__main__':
    # 创建milvus数据库
    # create_db('book')
    # db_name = 'book'
    # helper = MilvusHelper(host='127.0.0.1', port='19530', db_name=db_name)
    # helper.drop_collection('book')
    # create_collection(helper.client, 'book')
    # helper.describe_collection('book')
    # helper.load_collection('book')

    # 获取数据集
    # data = data.Data()
    # items = data.get_data_sets("book")
    # print(items[0])

    # 将数据暂存到sqlite中，后面逐条计算向量，然后逐条更新，重启后可恢复进度
    # SqliteDataBase.batch_save_items(items)

    # 获取Vector 为null 的数据进行处理
    items = SqliteDataBase.list_vector_null_items()
    print(len(items))
    transformer = Transformer.Transformer()
    for item in items:
        vector = transformer.get_embedding(item.strs)
        item.vector = vector
        (SqliteDataBase.Commands.update(
            {
                SqliteDataBase.Commands.vector: vector
            }
        )
         .where(SqliteDataBase.Commands.id == item.id)
         .execute())
