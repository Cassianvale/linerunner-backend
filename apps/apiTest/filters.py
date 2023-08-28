# -*-coding:utf-8 -*-

import django_filters
from .models import Api
class ApiFilter(django_filters.FilterSet):
    class Meta:
        models = Api
        fields = {
            'name':['icontains'],
        }