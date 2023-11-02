# linerunner-backend

![Static Badge](https://img.shields.io/badge/PYTHON%20-3.8-blue)    ![Static Badge](https://img.shields.io/badge/MYSQL%20-5.7-orange)


#### 部署环境

- python>=3.8.10  
- mysql==5.7  
- pip>=20.1.1  

#### 后端部署 

1. 创建并启用python虚拟环境(以下仅为vscode虚拟环境配置)  
* `cd linerunner-backend`  
* `python -m venv .venv`  
* `source .venv/Scripts/activate`  
2. 安装依赖(国内镜像源加速)  
`pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`  
3. 生成迁移脚本  
***ps: apps目录下的migrations文件夹不要删，不然执行迁移时会检索不到应用***  
`python manage.py makemigrations`  
4. 迁移数据库   
`python manage.py migrate`  
5. 初始化用户数据  (超管 admin  qa123456)
`python manage.py loaddata user`  
6. 运行  
`python manage.py runserver`  
7. 暂无前端页面，可以进入 http://127.0.0.1:8000/admin/  查看功能  

I.更新依赖文件  
`pip freeze > ./requirements.txt`  
II.异常情况清空数据库数据  
`python manage.py flush`  

![image](https://github.com/MuCqq/linerunner-backend/blob/a741827834137346c1f3fdbdd5fb586fa6c0823b/public/2024043.png?raw=true)