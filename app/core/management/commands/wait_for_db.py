# Test에서 사용할 wait_for_db command를 만들어야 함
# 그리고 나서 docker-compose에 내가 custom한 wait_for_db command 쓰겠다고
# command 섹션에 추가해야 함

import time
# DB 커넥션이 available한지 테스트 가능하게 해주는 모듈
from django.db import connections
# DB가 unavailable하면 던지는 에러
from django.db.utils import OperationalError
# custom command를 만들기 위한 BaseCommand
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Django command to pause execution until database is ready """

    # handleFunctiond은 이 management command를 실행할때마다 실행됨
    def handle(self, *args, **options):
        # stdout.즉 print함수랑 똑같음
        self.stdout.write('Waiting for database')
        db_conn = None
        while not db_conn:
            try:
                # get the database with keyword 'default' from settings.py
                db_conn = connections['default']
                """ connections['default'] calls the __getitem__ method 
                in ConnectionHandler class """
            except OperationalError:
                self.stdout.write('Database unavailable waiting one second...')
                # 프로덕션일땐 이런거 없지. 테스트하니까 그런 것
                time.sleep(1)

        # 녹색 메시지
        self.stdout.write(self.style.SUCCESS('Database available!'))

