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

TABLES = {}

TABLES['TableManager'] = (
    "CREATE TABLE `TableManager` ("
    "   `tableManagerId` int(11) NOT NULL AUTO_INCREMENT,"
    "   `tableName` varchar(50) DEFAULT NULL COMMENT '表名称',"
    "   `tableType` varchar(30) DEFAULT NULL COMMENT '表类型：中间表、维度表、查询表、事实表',"
    "   `dataLevel` varchar(50) DEFAULT NULL COMMENT '数据粒度：日汇总、周汇总、月汇总',"
    "   `procName` varchar(100) DEFAULT NULL COMMENT '所在过程',"
    "   `note` varchar(500) DEFAULT NULL COMMENT '表用途描述',"
    "   `inputMan` varchar(30) DEFAULT NULL COMMENT '创建人',"
    "   `inputDate` date DEFAULT NULL COMMENT '创建时间',"
    "   `updateMan` varchar(30) DEFAULT NULL COMMENT '最后更新人',"
    "   `updateTime` date DEFAULT NULL COMMENT '最后更新时间',"
    "   PRIMARY KEY (`tableManagerId`)"
    ") ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='表管理'")


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


def table_creation(cur):
    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name))
            cur.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
            return -1
        else:
            print("OK")

