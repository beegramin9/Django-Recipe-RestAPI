# admin Page unit test
""" Django Admin은 내 custom user model을 관리할수 있게 해준다.
로그인, 유저목록등을 관리할 수 있는 인터페이스를 제공한다. """

# Client는 http request를 가져옵니다.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Django Admin 페이지를 위한 Url 제공
from django.urls import reverse

class AdminSiteTests(TestCase):
    # setUp: TestCase 내의 모든 테스트가 실행되기 전에 실행되는 함수
    def setUp(self):
        """ 테스트에 쓰일 새 user 만듦 """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@londonappdev.com',
            password = 'password123'
        )
        # helper function임. 쟝고 authentication으로 로그인하게 함
        # 여기선 admin user가 client에 강제로 로그인됨
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@londonappdev.com',
            password = 'password123',
            name = "Test user full name"
        )

    def test_users_listed(self):
        # user들이 쟝고 admin의 user page에 등록되었는지 테스트
        """ 쟝고 디폴트 유저모델이 아이디가 username이었던것과 같이
        쟝고 admin도 아이디가 username이니 바꿔줘야 한다. 
        ==> admin.py 에 change들을 입력해야 함"""
        # 리스트 유저 페이지를 위한 url을 만들어줌
        url = reverse('admin:core_user_changelist')
        # HTTP get 요청
        res = self.client.get(url)
        
        # res 오브젝트 안에서 user.name이 있는지 알아서 확인함
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1, 왜? 만들어진 놈은 setUp에서 만들어진 한놈밖에 없음
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works """
        # 새로운 유저를 쟝고 admin에 등록하는 user page가 필요하다.
        # UserAdmin의 fieldset 아이디가 username으로 되어있어서 그럼
        # email로 바꿔줘야 한다 ==> admin.py에서 add_fieldset에 추가한다.
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)