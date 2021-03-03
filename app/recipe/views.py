# Tag앱을 위한 ViewSet

# 요기 viewsets, mixins엔 이름처럼 다양한 viewset, mixin 있음
# CUD 제외 R만 할거라서 GenericViewSet, ListModeMixin로 간단히 가능
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Manage tags in the database """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # list model할땐 모든 인스턴스틀 가져올 queryset 필요
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    """ AssertionError: 2 != 1 이 안나오려면
    Viewset에서 unauth user를 filter해줘야하는데 안함
    Viewset에 들어가면 queryset이 실행되고 밑에 filter customizing으로
    filter된 애들이 API에서 보일 것 """
    # overriding
    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        # request에 들어있는 user의 태그만
        # 즉 test에서 force_authenticate 된 setUp의 user만 통과
        return self.queryset.filter(user=self.request.user).order_by('-name')