FROM daocloud.io/centos:6
MAINTAINER  851125765@qq.com
RUN apt-get install python
COPY ./requirements
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["/app.py"]