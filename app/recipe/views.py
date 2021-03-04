# Tag앱을 위한 ViewSet

# 요기 viewsets, mixins엔 이름처럼 다양한 viewset, mixin 있음
# CUD 제외 R만 할거라서 GenericViewSet, ListModeMixin로 간단히 가능
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """ Base viewset for user owned recipe attributes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """ AssertionError: 2 != 1 이 안나오려면
    (user가 걸러지지 않아서 2개 다 들어옴)
    Viewset에서 unauth user를 filter해줘야하는데 안함
    Viewset에 들어가면 queryset이 실행되고 밑에 filter customizing으로
    filter된 애들이 API에서 보일 것 """
    # overriding
    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        # request에 들어있는 user의 attr만
        # 즉 test에서 force_authenticatioe된 setUp의 user만 들어옴
        return self.queryset.filter(user=self.request.user).order_by('-name')

    """ Create queryset을 지원하려면 이게 있어야 함
    이 함수는 object를 create할떄 실행되고 validated된 serializer가 pass됨 """
    def perform_create(self, serializer):
        """ Create a new object """
        # DB에서 create하니가 serializer 사용
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage tags in the database """
    # list model할땐 모든 인스턴스틀 가져올 queryset 필요
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredients in the database """
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer