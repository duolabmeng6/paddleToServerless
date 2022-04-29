FROM registry.cn-shenzhen.aliyuncs.com/duolabmeng/kunchongjiance:1.7

COPY app /app
WORKDIR /app

ADD /app/app_compat.py /usr/local/lib/python3.7/site-packages/paddlehub/serving/app_compat.py

#RUN pip install paddlex==2.1.0 -i https://mirror.baidu.com/pypi/simple
#RUN hub install /app/kunchongjiance.tar.gz
EXPOSE 9000

CMD ["/bin/bash","-c","hub serving start -m kunchongjiance -p 9000"]
