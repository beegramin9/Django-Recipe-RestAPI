from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

# Postgres DB가 준비되기 전에 쟝고가 불러 버려서 에러가 생기는 경우가 있다.
# 그걸 막기 위해서 wait_for_db 커맨드를 만듦
class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """ Test waiting for db when db is available """
        # DB가 available한지는 default db retrieve가 가능한지 안한지
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # 부를 때 사용되는 code 위치, 사용되는 함수 __getitem__
            
            # connection handler mocking
            # 임의로 True로 mocking함
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value = True)
    # 데코레이터를 사용하면 위 patch랑 똑같은 놈을 함수에 arg로 줘야 함
    # 여기 ts는 위 gi와 비슷한 놈
    # time.sleep을 그냥 true로 바꿔버림 ==> 이제 안 기다림, 테스트를 빠르게 하기 위해
    def test_wait_for_db(self, ts):
        """ Test waiting for db """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # mock 모듈은 sideeffect란게 있는데
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)