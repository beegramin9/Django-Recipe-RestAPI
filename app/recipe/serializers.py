from rest_framework import serializers
# Meta 클래스에서 model을 맞춰줘야 하기 때문에 대상 model import함
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag objects """
    
    class Meta:
        model = Tag
        fields = ('id', 'name')
        extra_kwargs = {
            'id' : {'read_only':True},
        }


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for ingredient objects """

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        extra_kwargs = {
            'id' : {'read_only': True}
        }

    
class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for recipe objects """

    # ingredients, tags는 Recipe 모델의 field가 아니니
    # Reference해줘야 한다
    ingredients = serializers.PrimaryKeyRelatedField(
        # Many to Many
        many = True, 
        # list ingredient objects with their primary key, id
        queryset = Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe 
        fields = ('id','title','ingredients','tags','time_minutes','price','link')
        extra_kwargs = {
            'id' : {'read_only': True}
        }