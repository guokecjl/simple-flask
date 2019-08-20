FROM python:3.6

WORKDIR /www

ADD . /www

RUN apt-get install -y git \
    && git submodule update --remote \
    && git submodule update \
    && cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD python start.py

EXPOSE 8888