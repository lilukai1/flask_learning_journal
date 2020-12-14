import datetime

from peewee import *

DATABASE = SqliteDatabase('social.db')


class Entry(Model):
    timestamp= DateTimeField(default=datetime.datetime.now)
    content = TextField()
    title = CharField()
    time_spent = IntegerField()
    resources = TextField()


    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()

