# -*-coding:utf-8 -*-


from io import BytesIO
import xlwt
import datetime
from apps.chanDao.models import ChanDaoCase
from rest_framework.views import APIView
from django.http import HttpResponse
from django.db.models import Model
from django.core.paginator import Paginator
from django.db.models.query import QuerySet


class DataDumpView(APIView):
    """将数据库记录转换为excel下载下来"""

    model = None  # 模型类,要导出的表
    order_field = ''  # 排序依据字段,只允许一个
    fields = '__all__'  # 表头以及字段，例{'num': '单号', 'price': '金额', 'add': '生单时间'}
    # __all__则代表所有，默认取verbose_name作为表头
    method_fields = {}  # 表中不存在的字段,需要自己实现对应的get__<字段名方法>
    exclude = []  # 将这些字段从要导出的字段中排除
    limit = 2000  # 当没有筛选条件时返回的记录条数
    sheet_size = 300  # 每个sheet记录数(不含表头)
    file_name = None  # 生成的xls文件名
    pk=0

    permission_classes = []  # 权限,此处要求子类必须覆盖，否则永远没有权限

    _protect_functions = ['get', ]

    def _get_paginator(self, queryset):
        """获取分页对象"""
        assert isinstance(queryset, QuerySet), (
            'queryset 必须是 Queryset类型，但是获取到一个{}'.format(type(queryset))
        )
        try:
            return Paginator(queryset.order_by(self.order_field), self.sheet_size)
        except:
            return Paginator(queryset, self.sheet_size)

    def get_queryset(self, request):
        """
        默认返回2000条数据
        如果需要筛选，则重写此方法
        """
        print(self.pk)
        if self.pk!=None:
            return self.model.objects.filter(modular__project__id=self.pk).order_by(self.order_field)[:self.limit]
        else:
            return self.model.objects.all().order_by(self.order_field)[:self.limit]
        # return self.model.objects.all().order_by(self.order_field)[:self.limit]

    def _get_method_fields(self, obj):
        """通过指定function获取表中不存在的值
            这个字段位于method_fields列表里面
        """
        for field in self.method_fields:
            func_name = 'get__{}'.format(field)
            if not hasattr(self, func_name):
                raise Exception(
                    '你在method_fields中定义了字段{},但是你并没有实现{}方法.'.format(
                        field,
                        func_name
                    )
                )
            setattr(obj, field, getattr(self, func_name)(obj))
        return obj

    def _get_relation_fields(self):
        """用于获取外键字段的属性"""
        raise Exception('这个方法将在下个版本实现')

    def get_format_value(self, obj, field):
        """将对象属性格式化"""
        attr = getattr(obj, field)
        value = attr
        # 外键格式化
        if isinstance(attr, Model):
            value = attr.__str__()
        # 时间类型格式化
        if isinstance(attr, datetime.datetime):
            value = attr.strftime('%Y-%m-%d %H:%M:%S')
        # 其他的暂时不做转换
        return value

    def _get_fields_map(self):
        """根据fields, exclude生成最终的fields_map"""
        fields_map = {}
        if self.fields == '__all__':
            # 获取所有字段
            fields_map = {field.name: field.verbose_name for field in self.model._meta.fields}
        elif isinstance(self.fields, dict):
            # 获取指定字段
            fields_map = self.fields
        # 要排除的字段
        del_keys = [field for field in self.fields if field in self.exclude]
        for d_k in del_keys:
            if d_k in fields_map:
                del fields_map[d_k]
        return fields_map

    def _get_file_io(self, request):
        """在io中生成excel文件"""
        x_io = BytesIO()  # io
        work_book = xlwt.Workbook()  # 工作簿
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'  # 指定“宋体”
        style.font = font
        queryset = self.get_queryset(request)
        paginator = self._get_paginator(queryset)

        for sheet in paginator.page_range:
            work_sheet = work_book.add_sheet(sheetname='sheet{}'.format(sheet))
            objs = paginator.page(sheet)
            row = 0
            for obj in objs:
                # 写下每一行
                col = 0
                fields_map = self._get_fields_map()
                # 获取obj通过method_fields获取的属性
                o = self._get_method_fields(obj)
                fields_map.update(self.method_fields)
                for field in fields_map:
                    # 填充单元格
                    if row == 0:
                        work_sheet.write(row, col, fields_map.get(field), style)
                        work_sheet.write(row+1, col, self.get_format_value(o, field), style)
                    else:
                        work_sheet.write(row+1, col, self.get_format_value(o, field), style)
                    col += 1
                row += 1
        work_book.save(x_io)
        return x_io
        # for sheet in paginator.page_range:
        #     work_sheet = work_book.add_sheet(sheetname='sheet{}'.format(sheet))
        #     objs = paginator.page(sheet)
        #     row = 0
        #     for obj in objs:
        #         # 写下每一行
        #         col = 0
        #         fields_map = self._get_fields_map()
        #         # 获取obj通过method_fields获取的属性
        #         o = self._get_method_fields(obj)
        #         fields_map.update(self.method_fields)
        #         for field in fields_map:
        #             # 填充单元格
        #             if row == 0:
        #                 work_sheet.write(row, col, fields_map.get(field), style)
        #             else:
        #                 work_sheet.write(row, col, self.get_format_value(o, field), style)
        #             col += 1
        #         row += 1
        # work_book.save(x_io)
        # return x_io

    def get_file_name(self):
        """获取生成文件的名字"""
        if self.file_name:
            return self.file_name
        elif hasattr(self.model, 'Meta'):
            if hasattr(self.model.Meta, 'verbose_name'):
                return self.model.Meta.verbose_name
        return self.model.__class__.__name__

    def _get_response(self, file_io, file_name):
        """得到响应对象"""
        res = HttpResponse()
        res["Content-Type"] = "application/vnd.ms-excel"
        res["Content-Disposition"] = 'attachment;filename={}.xls'.format(file_name).encode()
        res.write(file_io.getvalue())
        return res

    def get(self, request, pk=None):
        """主响应函数，接受GET请求"""
        # 在内存中准备好文件io
        #获取项目id，赋值给变量pk
        exec("self.pk={}".format(pk))
        file_io = self._get_file_io(request)
        file_name = self.get_file_name()
        # 确定响应
        response = self._get_response(file_io, file_name)
        return response