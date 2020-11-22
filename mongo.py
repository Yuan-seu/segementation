from pymongo import MongoClient
import pymongo
import datetime

"""
一个文件作为一个database输入
"""

client = MongoClient()


def database(data, name, error_number):
    """建立输入数据库"""
    keys = list(data.keys())
    db = client[name]
    for key in keys:
        collection(data[key], key, db, error_number)


def collection(data, name, db, error_number):
    """建立collection"""
    collections = db[name]
    for doc in data:
        document(doc, collections, error_number)


def document(data, coll, error_number):
    data['errornumber'] = error_number
    post_id = coll.insert_one(data).inserted_id


def input(data, name, error_number):
    '''输入数据，从这里开始'''
    database(data, name, error_number)
