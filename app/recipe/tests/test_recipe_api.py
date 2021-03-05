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

    # Creating recipes
    # django.db.utils.IntegrityError: null value in column "user_id" violates not-null constraint
    # create된 recipe object에 user가 연결이 안 되어있어서 그렇다
    # viewset에 perform_create override해야 함
    # perform_create는 auth된 user를 recipe의 user에 assign함
    def test_create_basic_recipe(self):
        """ Test creating recipe """
        payload = {
            'title':'Chocolate cheesecake',
            'time_minutes': 30,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data['id'])
        for key in payload.keys():
            # getattr: python helper function
            self.assertEqual(payload[key], getattr(recipe, key))
    
    def test_create_recipe_with_tags(self):
        """ Test creating a recipe with tags """
        tag1 = sample_tag(self.user, 'Vegan')
        tag2 = sample_tag(self.user, 'Dessert')
        payload = {
            'title':'Avocado lime cheesecake',
            # 왜 Id로 가져오지?
            'tags': [tag1.id, tag2.id],
            'time_minutes':60,
            'price':20.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data['id'])
        # recipe에 딸려 만들어진 tags retrieve
        # recipe object 안에 tags라는 key가 있네
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """ Test creating recipe with ingredients """
        ingredient1 = sample_ingredient(self.user, 'Prawns')
        ingredient2 = sample_ingredient(self.user, 'Ginger')
        payload = {
            'title' : 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price': 7.00
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    # Updating recipes
    """ Update는 ModelViewset에 빌트인되어있어서
    perform_create 안 넣어줘도 그냥 pass된다 """
    def test_partial_update_recipe(self):
        """ Test updating a recipe with PATCH """
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(self.user, "Curry")
        payload = {
            'title': 'Chicken tikka',
            'tags': [new_tag.id]
        }
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        # DB에서 update된 놈이랑 payload랑 맞는지
        # 그래서 res랑 비교 안하니까 res를 안 만듦 
        
        # model에 reference가 있을 떈 create할때마다
        # refresh를 해줘야지 바뀐다
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """ Test updating a recipe with PUT """
        recipe = sample_recipe(self.user)
        recipe.tags.add(sample_tag(self.user))
        payload = {
            'title':'Spaghetti carbonara',
            'time_minutes':25,
            'price':5.00
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        # payload에 tags가 없음
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)