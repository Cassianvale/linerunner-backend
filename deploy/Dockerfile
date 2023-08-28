FROM python:3.8

ENV LANG C.UTF-8
ENV TZ=Asia/Shanghai

# 记录当前使用时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /app/release
COPY ../deploy .
RUN  pip install -r ./requirements.txt -i \
    https://mirrors.aliyun.com/pypi/simple \
    --default-timeout=3000

CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
