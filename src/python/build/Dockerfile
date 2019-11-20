FROM python:3.6

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python3 \
    python3-dev\
    python3-pip\
    default-jdk

RUN pip3 install flask \
    Flask-Cors \
    bson \
    pymongo \
    requests 

RUN python -m pip install pymongo[srv]



EXPOSE 5000
WORKDIR /src/

CMD python3 app.py
