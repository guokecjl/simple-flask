# coding: utf-8

from pymongo import MongoClient
from urllib.parse import quote

from config import MONGO_CONFIG


def conn_mongodb(db_config):
    """
    连接mongodb
    """
    host_port = ','.join(["{0}:{1}".format(quote(host), quote(
        str(port))) for host, port in db_config['host_port']])

    auth_db = quote('admin')
    database = quote(db_config['database'])
    username = quote(db_config['user_name'])
    password = quote(db_config['password'])

    if username and password and auth_db:
        uri = "mongodb://%s:%s@%s/%s" % (username,
                                         password, host_port, auth_db)
    else:
        uri = "mongodb://%s" % host_port

    return MongoClient(uri)[database]


account_mgo = conn_mongodb(MONGO_CONFIG['account'])
admin_mgo = conn_mongodb(MONGO_CONFIG['admin'])
