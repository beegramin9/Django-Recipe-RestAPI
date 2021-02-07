# Docker가 Dockerfile에 있는 dependencies를 읽고 Image를 만든다.
FROM python:3.7-alpine
# 첫번째 줄은 Dockerfile이 상속할 이미지이다.
# 상속하고 나서 내가 커스터마이징하면 된다.


ENV PYTHONUNBUFFERED 1
# Unbuffered: 다른곳에 데이터를 저장하고 가져오는 게 아니라 바로 Print한다.
# Docker로 Python 돌릴 때 에러 날 확률 적음

COPY ./requirements.txt /requirements.txt
# package.json처럼 requirements.txt에 dependencies를 저장한다.
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

