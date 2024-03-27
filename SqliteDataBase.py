from peewee import *
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db = SqliteDatabase('temp.db')


def batch_save_items(items):
    for batch in chunked(items, 1000):
        Commands.insert_many(batch).execute()


# noinspection PyComparisonWithNone
def list_vector_null_items():
    return Commands.select().where(Commands.vector == None)


class Commands(Model):
    id = AutoField()
    objective = TextField(null=True)
    command_name = TextField(null=True)
    command = TextField(null=True)
    syntax = TextField(null=True)
    flags = TextField(null=True)
    description = TextField(null=True)
    question = TextField(null=True)
    strs = TextField(null=True)
    vector = TextField(null=True)

    class Meta:
        database = db  # This model uses the "people.db" database.


if __name__ == '__main__':
    db.connect(True)
    db.create_tables([Commands], safe=True)
