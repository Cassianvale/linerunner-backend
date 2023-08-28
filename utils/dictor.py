# -*-coding:utf-8 -*-
from __future__ import print_function
import json

"""
从字典中获取指定路径下的值。它的作用是根据给定的路径，从一个嵌套的字典或列表中获取对应的值

"""
def dictor(data, path=None, default='', checknone=False, ignorecase=False, pathsep="."):
    '''
    Usage:
    get a value from a Dictionary key
    > dictor(data, "employees.John Doe.first_name")

    parse key index and fallback on default value if None,
    > dictor(data, "employees.5.first_name", "No employee found")

    pass a parameter
    > dictor(data, "company.{}.address".format(my_company))

    if using Python 3, can use F-strings to pass parameter
    > param = 'MyCompany'
    > dictor(data, f"company.{param}.address")

    lookup a 3rd element of List, on second key, lookup index=5
    > dictor(data, "3.first.second.5")

    lookup a nested list of lists
    > dictor(data, "0.first.1.2.second.third.0.2"

    check if return value is None, if it is, raise an error
    > dictor(data, "some.key.value", checknone=True)
    > ValueError: value not found for search path: "some.key.value"

    ignore letter casing when searching
    > dictor(data, "employees.Fred Flintstone", ignorecase=True)
    '''

    if path is None or path == '':
        return data

    try:
        for key in path.split(pathsep):
            if isinstance(data, (list, tuple)):
                val = data[int(key)]
            else:
                if ignorecase:
                    for datakey in data.keys():
                        if datakey.lower() == key.lower():
                            key = datakey
                            break
                val = data[key]
            data = val
    except (KeyError, ValueError, IndexError, TypeError):
        val = default

    if checknone:
        if not val or val == default:
            raise ValueError('value not found for search path: "%s"' % path)
    return val