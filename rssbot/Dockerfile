FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN mkdir /app && mkdir /resources
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN sed -i s#https://#http://#g /usr/local/lib/python3.8/dist-packages/sym_api_client_python/configure/configure.py
WORKDIR /app
COPY app/ . 
COPY resources/* /resources/
USER 1000
CMD ["python3", "main_async.py"]

