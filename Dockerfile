FROM python:3.7.6-alpine3.11
LABEL maintainer="gunkow@gmail.com"
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY  temporary.py .

CMD python /usr/src/app/temporary.py