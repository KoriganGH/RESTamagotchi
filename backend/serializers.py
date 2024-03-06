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


class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class UserStorageFoodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorageFood
        fields = "__all__"


class UserStorageSkinDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStorageFood
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


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
        fields = ('code',)
