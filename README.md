# LineRunner-Backend

#### 部署环境

python==3.8.10  
mysql==5.7  
pip==20.1.1

#### 后端部署 

1.创建环境  
`cd linerunner-backend`  
`python -m venv .venv`  
2.启动虚拟环境  
`source .venv/Scripts/activate`  
3.安装虚拟环境  
`pip install -r requirements.txt`  
4.生成迁移脚本  
`python manage.py makemigrations`  
5.迁移数据库   
`python manage.py migrate`  
6.创建超级用户  
`python manage.py createsuperuser`  
7.初始化用户数据  
`python manage.py loaddata user`  
8.运行  
`python manage.py runserver`  
9.更新依赖文件  
`pip freeze > ./requirements.txt`  
10.异常情况清空数据库数据  
`python manage.py flush`  
