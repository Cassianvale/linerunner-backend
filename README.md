# LineRunner-Backend

![Static Badge](https://img.shields.io/badge/PYTHON%20-3.8-blue)    ![Static Badge](https://img.shields.io/badge/MYSQL%20-5.7-orange)


#### 部署环境

- python>=3.8.10  
- mysql==5.7  
- pip>=20.1.1  

#### 后端部署 

1.创建并启用python虚拟环境  
`cd linerunner-backend`  
`python -m venv .venv`  
`source .venv/Scripts/activate`  
2.安装依赖(国内镜像源加速)  
`pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`  
3.生成迁移脚本  
`python manage.py makemigrations`  
4.迁移数据库   
`python manage.py migrate`  
5.创建超级用户  
`python manage.py createsuperuser`  
6.初始化用户数据  
`python manage.py loaddata user`  
7.运行  
`python manage.py runserver`  

I.更新依赖文件  
`pip freeze > ./requirements.txt`  
II.异常情况清空数据库数据  
`python manage.py flush`  
