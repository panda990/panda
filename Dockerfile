FROM liker5092/python3-nginx-uwsgi
WORKDIR /root
COPY . /root
EXPOSE 80
RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN apt-get install -y libglib2.0-dev
WORKDIR /root
RUN pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
CMD python3 app.py
