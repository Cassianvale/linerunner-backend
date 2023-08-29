# Generated by Django 3.1.2 on 2021-02-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chanDao', '0004_auto_20210224_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chandaocase',
            name='case_priority',
            field=models.IntegerField(choices=[['功能测试阶段', '功能测试阶段'], ['系统测试阶段', '系统测试阶段'], ['冒烟测试阶段', '冒烟测试阶段']], default='3', max_length=10, verbose_name='优先级'),
        ),
    ]