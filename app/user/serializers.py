from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the users object """
    class Meta:
        # serializer가 어떤 모델을 대상으로 하는지 configure
        model = get_user_model()
        # API에서 accessible한 /DTO 할 field configure
        fields = ('email','password','name')
        extra_kwargs = {
            'password' : {'write_only':True, 'min_length': 5},
        }

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        # User가 생성될 때 data를 validate해서 인자에 전달
        # 즉, create/update funciton이 DTO 역할을 함
        return get_user_model().objects.create_user(**validated_data)

        