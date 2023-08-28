#!/usr/bin/python
# encoding=utf-8
import pymysql

pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()
