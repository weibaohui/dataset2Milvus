import time

import SqliteDataBase
import Transformer

transformer = Transformer.Transformer()


def calc_zh_vector():
    items = SqliteDataBase.Commands.select().where(SqliteDataBase.Commands.zh_vector == None,
                                                   SqliteDataBase.Commands.zh_strs != None).dicts()
    items = list(items)
    for i, item in enumerate(items):
        print(f'{i + 1}/{len(items)}')
        # 对中英文描述 合并计算向量
        vector = transformer.get_embedding(item['zh_strs'] + '\n' + item['strs'])
        (SqliteDataBase.Commands.update(
            {
                SqliteDataBase.Commands.vector: vector,
                SqliteDataBase.Commands.zh_vector: True
            }
        )
         .where(SqliteDataBase.Commands.id == item['id'])
         .execute())


if __name__ == '__main__':
    for i in range(10000):
        print(f'第{i + 1}次计算')
        calc_zh_vector()
        time.sleep(30)
