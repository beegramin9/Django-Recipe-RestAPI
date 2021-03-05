from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

# -list: listing API
# /api/recipe/recipes
RECIPE_URL = reverse('recipe:recipe-list')

# /api/recipe/recipes/1
def detail_url(recipe_id):
    """ Return recipe detail URL """
    return reverse("recipe:recipe-detail", args=[recipe_id])



# Sugar syntax
def sample_tag(user, name = "Main course"):
    """ Create and return a sample tag """
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name = "Cinnamon"):
    """ Create and return a sample ingredient """
    return Ingredient.objects.create(user=user, name=name)

def sample_recipe(user, **params):
    """ Create and return a sample recipe """
    defaults = {
        'title':'Sample recipe',
        'time_minutes': 10,
        "price": 5.00
    }
    # Param에 실제 값이 들어와서 defaults를 customize해야 할떈?
    # Python dictionary의 update function으로
    defaults.update(params)

    # **defaults: defaults dictionary를 arguments로
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ Test unauthenticated recipe API access """

    def setUp(self):
        self.client = APIClient()
        
    def test_auth_required(self):
        """ Test that authentication is required """
        # unauthenticated request
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """ Test unauthenticated recipe AIP access """
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """ Test retrieving a list of recipes """
        sample_recipe(user = self.user)
        sample_recipe(user = self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        # DB에서 가져왔으니 JSON으로
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # List API의 recipe와 DB에서 가져온 recipe가 같은지
        self.assertEqual(res.data, serializer.data)


    def test_recipes_limited_user(self):
        """ Test retrieving recipes for user """
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'password123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user = self.user)
        # object가 하나밖에 없어도 list API의 데이터는
        # object의 list여야 함
        serializer = RecipeSerializer(recipes, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    # Detailed Recipe Tests
    def test_view_recipe_detail(self):
        """ Test viewing a recipe detail """
        recipe = sample_recipe(user=self.user)
        # recipe에 tag와 ingredient 정보 추가
        # many-to-many field에 item 더하는 법
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)
        # List를 하고싶었던 list view와는 달리 object 하나만 가져옴
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)