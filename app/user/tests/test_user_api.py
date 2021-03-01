""" 새 Test를 만들면
Test를 시행하게 될 Url(=reverse('user:create')을 만들 View를,
이 url에 DTO 역할을 할 Serializer를,
그리고 url을 메인 앱의 urls.py 에 연결해야 한다 """
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# API로 전달된 HTTP request를 가져옵니다
from rest_framework.test import APIClient
# request status code를 가져옵니다
from rest_framework import status

# Constant Variable
CREATE_USER_URL = reverse('user:create')

# example로 쓸 user를 만들 Helper function/ sugar syntax
def create_user(**params):
    return get_user_model().objects.create_user(**params)

# Unauthenticated = Public 
class PublicUserApiTests(TestCase):
    """ Test the users API (public) """
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succeeded(self):
        """ Test creating user with valid payload is successful """
        # payload: API에 request를 보낼 때 같이 보내는 object
        payload = {
            'email':'Test@londonappdev.com ',
            'password':'testpass',
            'name':'Test name'
        }
        # API에 request 보내기
        res = self.client.post(CREATE_USER_URL, payload)

        # 1. post request니 status_code = 201여야 함
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # 2. user가 실제로 만들어졌는지 테스트
        # post로 유저가 만들어졌을 때, 새 user를 return값으로 주는 것을 이용
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # return값으로 password가 들어오지 않는지 확인
        self.assertNotIn('password',res.data)

    def test_user_exists(self):
        """ Test creating user that already exists fails """
        payload = {
            'email':'Test@londonappdev.com ',
            'password':'testpass',
            'name':'Test name'
        }            
        # 위의 Helper function 사용
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters """
        payload = {
            'email':'Test@londonappdev.com ',
            'password':'pwd',
            'name':'Test name'
        }   
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # user가 만들어지지 않았는지 테스트
        """ 매 테스트 function마다 DB가 refresh되기 때문에
        test_create_valid_user_succeeded에서 만들어진 user가 남아있지 않다 """
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)


    pass
# Authenticated = Private 
class PrivateUserApiTest(TestCase):
    pass