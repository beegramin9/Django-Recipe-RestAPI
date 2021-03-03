from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """ Test the publicly available tags API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving tags """
        # unauth된 request를 보냄
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Test the authorizeds user tags API """

    def setUp(self):
        # auth할때 쓸 user
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password123'
        )
        self.client = APIClient()
        # 모든 request를 위에 만든 sample user로 authenticate
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retrieving tags """
        # sample tags들을 먼저 몇개 만든 후
        # API에 request를 보내고
        # request 내의 tag와 내 tag가 같은지
        Tag.objects.create(user= self.user, name='Vegan')
        Tag.objects.create(user= self.user, name='Dessert')
        res = self.client.get(TAGS_URL)
        # - 붙여서 reversed alphabetical order
        tags = Tag.objects.all().order_by('-name')

        # tag를 serialize함( DB에서 받아왔으니 JSON으로)
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    # auth된 user의 tag만 들어오는지 테스트
    def test_tags_limited_to_user(self):
        """ Test that tags returned are for the authenticated user """
        # setup에서 만든 user 말고 새 user(unathenticated) 만든 후
        # 새 유저에 만들어논 tag를 assign
        # 이 tag들은 request에 안 담겨져오길 예상
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Tag.objects.create(user = user2, name = "Fruity")
        tag = Tag.objects.create(user = self.user, name = "Comfort Food")

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 1개 들어와야 함. 1개만 auth user니까
        self.assertEqual(len(res.data), 1)
        # response의 tag가 우리가 assign한게 맞는지
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """ Test creating a new tag """
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user = self.user,
            name = payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """ Test creating a new tag with invalid payload """
        payload = {'name': ''}
        
        res = self.client.post(TAGS_URL, payload)
        # 맨 처음 할때는 400 대신 405가 들어오는데
        # views.py에서 ViewSet의 ListModelMixin에 CreateModelMixin을 추가해야 한다.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)