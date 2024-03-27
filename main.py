import json

from peewee import chunked
from pymilvus import MilvusClient, DataType

import SqliteDataBase
import Transformer
from milvus_helper import MilvusHelper

DB_NAME = 'book'
COLLECTION_NAME = 'book'
helper = MilvusHelper(host='127.0.0.1', port='19530', db_name=DB_NAME)


def create_collection(client: MilvusClient, collection_name: str):
    # 3.1. Create schema
    schema = client.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )

    # 3.2. Add fields to schema
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
    schema.add_field(field_name="objective", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
    schema.add_field(field_name="command_name", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
    schema.add_field(field_name="command", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
    schema.add_field(field_name="description", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
    schema.add_field(field_name="syntax", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
    schema.add_field(field_name="flags", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
    schema.add_field(field_name="question", datatype=DataType.VARCHAR, max_length=65535, is_nullable=True)
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


def import_dataset_to_milvus():
    # 1.获取数据集
    # data = data.Data()
    # items = data.get_data_sets("book")
    # print(items[0])
    # 2.将数据暂存到sqlite中，后面逐条计算向量，然后逐条更新，重启后可恢复进度
    # SqliteDataBase.batch_save_items(items)
    # 3.获取Vector 为null 的数据进行处理
    # items = SqliteDataBase.list_vector_null_items()
    # print(len(items))
    # transformer = Transformer.Transformer()
    # for item in items:
    #     vector = transformer.get_embedding(item.strs)
    #     item.vector = vector
    #     (SqliteDataBase.Commands.update(
    #         {
    #             SqliteDataBase.Commands.vector: vector
    #         }
    #     )
    #      .where(SqliteDataBase.Commands.id == item.id)
    #      .execute())
    # 4.将sqlite中的数据，导入到milvus 中
    # 4.1创建milvus数据库
    # helper.create_db(DB_NAME)
    helper.drop_collection(COLLECTION_NAME)
    create_collection(helper.client, COLLECTION_NAME)
    helper.describe_collection(COLLECTION_NAME)
    # 4.2 从sqlite中查询数据,插入milvus
    items = SqliteDataBase.Commands.select().dicts()
    items = list(items)
    for item in items:
        del item['id']
        del item['strs']
        item['vector'] = json.loads(item['vector'])
        # None 类型转换为str
        if item['question'] is None or len(item['question']) == 0:
            item['question'] = ''
    # 4.2.1 批量插入数据,适合生产,按1000条为一批进行插入
    for batch in chunked(items, 1000):
        helper.insert(COLLECTION_NAME, batch)
    # 4.2.2 逐条插入数据，适合调试
    # for item in items:
    #     try:
    #         helper.insert(COLLECTION_NAME, item)
    #     except Exception as e:
    #         print(item)
    #         print(e)
    # 4.3 查看milvus中的数据
    helper.describe_collection(COLLECTION_NAME)
    helper.load_collection(COLLECTION_NAME)


def search_with_transformer(search_text: str):
    transformer = Transformer.Transformer()
    print(f'我想要:\t{search_text}')
    search_vector = transformer.get_embedding(search_text)
    res = helper.client.search(
        collection_name=COLLECTION_NAME,  # Replace with the actual name of your collection
        # Replace with your query vector
        data=[search_vector],
        limit=1,  # Max. number of search results to return
        search_params={"metric_type": "IP", "params": {}}  # Search parameters
    )
    # Convert the output to a formatted JSON string
    result = json.dumps(res, indent=4)
    # print(result)
    ids_list = [item['id'] for item in res[0]]
    # print(ids_list)
    res = helper.client.get(
        collection_name=COLLECTION_NAME,
        ids=ids_list
    )
    for item in res:
        print(f'参考命令:\t{item['command']}')
        print(f'请给我一个完整的具体的可执行的命令，只要命令本身，其他啥都不要返回')


if __name__ == '__main__':
    # import_dataset_to_milvus()
    search_with_transformer('创建一个名为xyz的namespace')
    pass
