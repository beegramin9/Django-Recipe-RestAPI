""" Test에서 reverse로 새 url을 만들면
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
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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
            'email':'Test@londonappdev.com',
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
            'email':'Test@londonappdev.com',
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
            'email':'Test@londonappdev.com',
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

    # 새 auth를 만드는 것이기때문에 public 아래로
    def test_create_token_for_user(self):
        """ Test that a token is created for the user """
        payload = {
            'email':'Test@londonappdev.com',
            'password':'testpass',
            'name':'Test name'
        }   
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # 성공적으로 create 되었다면 token이 있을 것, 빌트인 쟝고 auth
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given """
        create_user(email='Test@londonappdev.com', password='testpass')
        # 잘못된 Password
        payload = {
            'email':'Test@londonappdev.com',
            'password':'wrong',
            'name':'Test name'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test that token is not created if user doesn't exist """
        payload = {
            'email':'Test@londonappdev.com',
            'password':'testpass',
            'name':'Test name'
        }
        # 여기선 create_user()로 새 user를 만들지 않음
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        res = self.client.post(TOKEN_URL, {'email':'one', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # unauth된 user가 사용하는 것을 가정
    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users  """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Authenticated = Private 
# Auth된 user가 사용하는 것을 가정
# edit만 지원할 것이기에 post는 지원안할것, patch와 put만 할 것
class PrivateUserApiTest(TestCase):
    """ Test API requests that require authentication """
    def setUp(self):
        self.user  = create_user(
            email = 'test@londonappdev.com',
            password = 'testpass',
            name = 'name'
        )
        self.client = APIClient()
        # 모든 request를 위에 만든 sample user로 authenticate
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # res의 user와 auth된 user가 같은지 확인
        # res엔 password를 보내지 않는다
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
    
    def test_post_me_not_allowed(self):
        """ Test that POST request is not allowed on ME_URL """
        # Post 에 아무것도 보내지 않는다
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = {
            'name': 'new name',
            'password': 'newpassword123'
        }
        res = self.client.patch(ME_URL, payload)
        # 쟝고 ORM, user 정보를 업뎃했으니 업뎃된 정보를 db에서 가져옴
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
