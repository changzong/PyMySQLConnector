# __author__ = ''
# -*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import errorcode


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


def database_removal(cur, row_id):
    try:
        print 'Removing row from table'
        cur.execute("""
           DELETE FROM TableManager
           WHERE tableManagerId=%s
        """, row_id)
        print 'Removing finished.'
    except mysql.connector.Error as err:
        print err.message
        return -1
    else:
        print 'OK'


def database_restructure(cur, row_id_str, count):
    try:
        print 'Updating IDs from table'
        print row_id_str, count
        for i in range(int(row_id_str), count):
            cur.execute("""
               UPDATE TableManager
               SET tableManagerId=%s
               WHERE tableManagerId=%s
            """, tuple([str(i), str(i+1)]))
        print 'Updating finished'
    except mysql.connector.Error as err:
        print err.message
        return -1
    else:
        print 'OK'
