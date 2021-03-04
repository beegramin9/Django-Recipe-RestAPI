from django.urls import path, include

# viewset을 위한 url을 자동적으로 generate
from rest_framework.routers import DefaultRouter
# viewset 하나에 많은 view들이 associated
# view와 달리 viewset은 router로 url에 연결한다
# 각 action에 맞는 url을 할당한다

from recipe import views

router = DefaultRouter()
# 연결할 url 이름, base_name은 url 가져올때 사용됨
# register하면 recipe url에 적용이 되는 것
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    # Viewset의 url include
    path('', include(router.urls)),
]