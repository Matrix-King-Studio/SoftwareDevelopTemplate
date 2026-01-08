FROM python:3.10

# 更新包列表
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        default-libmysqlclient-dev

# 修改时区为国内时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip setuptools wheel

# 安装必要的项目依赖
WORKDIR /app/Backend
ADD ./requirements.txt /app/Backend/requirements.txt
RUN pip install --retries 5 --timeout 120 -r requirements.txt

ADD ./ /app/Backend
RUN mkdir -p /usr/local/var/log/django
