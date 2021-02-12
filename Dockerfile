# 새로운 docker 가상환경 build 명령어
# sudo docker-compose build

# Docker가 Dockerfile에 있는 dependencies를 읽고 Image를 만든다.
FROM python:3.7-alpine
# 첫번째 줄은 Dockerfile이 상속할 이미지이다.
# 상속하고 나서 내가 커스터마이징하면 된다.


ENV PYTHONUNBUFFERED 1
# Unbuffered: 다른곳에 데이터를 저장하고 가져오는 게 아니라 바로 Print한다.
# Docker로 Python 돌릴 때 에러 날 확률 적음

COPY ./requirements.txt /requirements.txt
# --update는 레지스트리 업데이트(= sudo apt update)
# --no-cache, 레지스트리 인덱스 저장 안함 ==> 패키지 최소화로 설치
RUN apk add --update --no-cache postgresql-client

# temporary requirements, 맨 처음 할때만 필요
# virtual: 디펜던시 별명 설정
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

# package.json처럼 requirements.txt에 dependencies를 저장한다.
# 추가하려면 requirements.txt 위에 적어야 함
RUN pip install -r /requirements.txt

# temporary requirements 제거
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user