
from unittest import TestCase, main
from unittest.mock import patch

def hello():
    return 'Hello!'

class TestMe(TestCase):
    # @patch로 데코레이팅 된 함수/클래스만 Mocking
    """ 첫번째 인자: patching할 메소드를 package.module.Class.method 형태로 
    같은 모듈(py파일)에 있다면 __main__ 
    두번째 인자: return_value, 선택적
    """

    @patch('__main__.hello', return_value = "Mock!")
    # @patch 데코레이터는 MagicMock 객체를 테스트 함수의 인자로 추가합니다
    # 즉, mock_hello라는 변수에 객체를 저장합니다.
    def test_hello(self, mock_hello):
        self.assertEqual(hello(), "Mock!")
        # hello 메소드와 mock_hello 변수에 담긴 MagickMock 객체가 같은지?
        # 즉, MagicMock 객체가 제대로 hello 메소드를 Mocking했는지?
        self.assertIs(hello, mock_hello)
        mock_hello.assert_called_once_with()

if __name__ == "__main__":
    main()
