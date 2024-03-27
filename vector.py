import SqliteDataBase
import Transformer


def calc_zh_vector():
    items = SqliteDataBase.Commands.select().where(SqliteDataBase.Commands.zh_vector == None and SqliteDataBase.Commands.zh_strs != None ).dicts()
    items = list(items)
    transformer = Transformer.Transformer()
    for i, item in enumerate(items):
        print(f'{i}/{len(items)}')
        # 对中英文描述 合并计算向量
        vector = transformer.get_embedding(item['zh_strs']+'\n'+item['strs'])
        (SqliteDataBase.Commands.update(
            {
                SqliteDataBase.Commands.vector: vector,
                SqliteDataBase.Commands.zh_vector: True
            }
        )
         .where(SqliteDataBase.Commands.id == item['id'])
         .execute())


if __name__ == '__main__':
    calc_zh_vector()
