from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

# 빌트인 View
# serializer를 이용해서 DB에 인스턴스를 create하는 API를 만듦
class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer

# 빌트인 View
class CreateTokenView(ObtainAuthToken):
    """ Creata a new auth token for user """
    serializer_class = AuthTokenSerializer

    # Override해서 새로 정의해서 browsable 하게 만듦
    # ViewSet과 Url View들을 모아 볼수 있는 Hub
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    # permissions: level of access user has
    # user는 auth되어야지만 api 사용가능하게 함
    permission_classes = (permissions.IsAuthenticated, )

    # API View에서는 한 model과 연결하고
    # model의 한 객체를 가져올 수 있게 해야함
    # 여기선 logged in된 user를 위한 User 모델을 가져올 것

    # 따라서 default get_object를 override 
    def get_object(self):
        """ Retrieve and return authentication user """
        # 그냥 User 객체가 아니라 authenticated 된 User를 리턴
        # 그냥 user인것같은데 이게 어떻게 되지?
        # auth_class가 알아서 unauth된 유저를 request에 assign해주기 때문
        # get_object가 called되면 request에 user가 같이 들어온다
        return self.request.user