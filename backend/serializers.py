from rest_framework import serializers
from .models import *


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class CategoryFoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryFood
        fields = "__all__"


class PersonalityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = "__all__"


class SkinDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skin
        fields = "__all__"


class PetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"


class PetPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['mood_points', 'purity_points', 'starvation_points']


class PetPointsIncreaseSerializer(serializers.Serializer):
    pet_id = serializers.IntegerField()
    characteristic = serializers.CharField()
    value = serializers.IntegerField()


class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class UserStorageFoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorageFood
        fields = "__all__"


class BuyFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorageFood
        fields = "user", "food"


class UserStorageSkinDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorageSkin
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserEditBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "id", "balance"

    id = serializers.IntegerField(required=True)


class UserSetNickSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "id", "name"

    id = serializers.IntegerField(required=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"


class AuthenticationCodeSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationCode
        fields = ('phone_number',)


class AuthenticationCodeVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationCode
        fields = ('phone_number', 'code')
