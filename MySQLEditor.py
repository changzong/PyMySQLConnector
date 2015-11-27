# __author__ = ''
# -*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import errorcode


config = {
    'user': 'xxx',
    'password': 'xxx',
    'host': 'xxx',
    'database': 'xxx',
    'use_pure': True  # The default is True which means using pure Python rather than C extensions
}


def database_connection(configuration):
    try:
        cnx = mysql.connector.connect(**configuration)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return -1
    else:
        return cnx


def database_edition(cur, table_data):
    try:
        print 'Editing new information into table'
        cur.execute("""
           UPDATE TableManager
           SET tableName=%s, tableType=%s, dataLevel=%s, procName=%s, note=%s, inputMan=%s, inputDate=%s, updateMan=%s, updateDate=%s
           WHERE tableManagerId=%s
        """, table_data)
        print 'Executing finished.'
    except mysql.connector.Error as err:
        print err.message
        return -1
    else:
        print 'OK'
