from rest_framework import generics
from user.serializers import UserSerializer

# 빌트인 View
# serializer를 이용해서 DB에 인스턴스를 createg하는 API를 만듦
class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer