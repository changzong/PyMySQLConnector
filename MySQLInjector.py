# __author__ = 'ZongChang'
# -*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import errorcode


config = {
    'user': 'bigdata',
    'password': '4WsiKvxhi9pITBfO4Mc8',
    'host': '10.33.64.15',
    'database': 'report',
    'use_pure': True  # The default is True which means using pure Python rather than C extensions
}


add_employee = ("INSERT INTO TableManager "
               "(tableManagerId, tableName, tableType, dataLevel, procName, note, inputMan, inputDate, updateMan, updateDate)"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

# Sdata_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))


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


# def table_insertion(cur):


