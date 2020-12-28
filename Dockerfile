FROM daocloud.io/centos:6
MAINTAINER  851125765@qq.com
RUN pip install -r requirements.txt
COPY . /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["/app.py"]