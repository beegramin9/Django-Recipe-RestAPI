# Tests 폴더에 모든 test 파일 모아놓기
from django.test import TestCase

# get_user_model helper function (쟝고 내장)
# 내장 usermodel보다 get_user_model을 더 추천함
# get_user_model은 settings.py의 AUTH_USER_MODEL = "core.User"에 명시된
# customized된 User 모델을 불러온다.
from django.contrib.auth import get_user_model
""" create_user(helper function)이 새로운 user를 잘 만드는지를 test """

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email succeeded. """
        email = "test@londonappdev.com"
        password = "Testpass123"


        # print(get_user_model().objects)
        """ get_user_model() == class 'core.models.user' """

        # 내 User모델의 create_user 메소드를 그대로 가져와서 쓰는 것
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        # assert: 테스트 할 때 (사실임을) 주장하다.
        self.assertEqual(user.email, email)
        # password는 encrypted 되기 때문에 email처럼 할 수 없다.
        # check_password는 Django helper function, boolean을 return한다.
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized. """
        email = "test@LONDONAPPDEV.COM"
        user = get_user_model().objects.create_user(email,'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """ Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        # User에 is_superuser를 더하지 않았지만 PermissionsMixin에 기본으로 있음
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

""" 
이거 달면 그냥 python my_tests.py 로만 써도 된다는데?
if __name__ == '__main__':
    main() """