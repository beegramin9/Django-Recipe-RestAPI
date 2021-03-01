from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

# 빌트인 View
# serializer를 이용해서 DB에 인스턴스를 create하는 API를 만듦
class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer

# 빌트인 View
# 
class CreateTokenView(ObtainAuthToken):
    """ Creata a new auth token for user """
    serializer_class = AuthTokenSerializer

    # Override해서 새로 정의해서 browsable 하게 만듦
    # ViewSet과 Url View들을 모아 볼수 있는 Hub
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    