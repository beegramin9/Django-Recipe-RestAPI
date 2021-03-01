""" We may not want to actually connect to a database while testing. 
In such cases, we can mock a database connection 
https://www.mlr2d.org/modules/djangorestapi/09_command_to_wait_for_db
"""

from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

# Postgres DB가 준비되기 전에 쟝고가 불러 버려서 에러가 생기는 경우가 있다.
# 그래서 서버 연결하기 전에 DB가 available한지 확인하기 위해 wait_for_db 커맨드를 만듦
class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """ Test if the connection works when db is available """
        # DB가 available한지는 default db retrieve가 가능한지 안한지

        """  Mock is used to change the default return value of a method at certain parts of the code
        mock을 하기 위해 db와 connection하는 코드를 찾음 """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # 부를 때 사용되는 code 위치, 사용되는 함수 __getitem__
            
            # connection handler mocking
            # 임의로 True로 mocking함
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value = True)
    def test_wait_for_db(self, mock_time_sleep):
        """ Test if connection works when db is not connected """
        # 원래는 DB가 unavailable하면 1초동안 sleep을 하는데
        # 테스트할 떄는 굳이 기다릴 필요 없으니 안 기다림 ==> time.sleep을 그냥 true로 바꿔버림
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # make the patch return error for first five calls
            # and return true on sixth call 
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
