# -*-coding:utf-8 -*-

from django.db import connection
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'linerunner.settings'

def my_custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    