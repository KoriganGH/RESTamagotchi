from django.db import models
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'


class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    saturation = models.IntegerField()

    class Meta:
        db_table = 'food'


class CategoryFood(models.Model):
    category = models.OneToOneField(Category, models.CASCADE, primary_key=True)
    food = models.ForeignKey(Food, models.CASCADE)

    class Meta:
        db_table = 'categories_food'
        unique_together = (('category', 'food'),)


class Personality(models.Model):
    personality = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(Category, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'personality'


class Skin(models.Model):
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'skin'


class Pet(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=True, null=True)
    is_male = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey('UserProfile', models.CASCADE, blank=False, null=False)
    personality = models.ForeignKey(Personality, models.SET_NULL, blank=True, null=True)
    mood_points = models.IntegerField(default=100, blank=True, null=True, validators=[
        MaxValueValidator(100), MinValueValidator(0)])
    purity_points = models.IntegerField(default=100, blank=True, null=True, validators=[
        MaxValueValidator(100), MinValueValidator(0)])
    starvation_points = models.IntegerField(default=100, blank=True, null=True, validators=[
        MaxValueValidator(100), MinValueValidator(0)])


    class Meta:
        db_table = 'pet'


class Game(models.Model):
    points = models.IntegerField()
    user = models.ForeignKey('UserProfile', models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'game'


class UserStorageFood(models.Model):
    user = models.ForeignKey('UserProfile', models.CASCADE, blank=True, null=True)
    food = models.ForeignKey(Food, models.CASCADE, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        db_table = 'user_storage_food'


class UserStorageSkin(models.Model):
    user = models.ForeignKey('UserProfile', models.CASCADE)
    skin = models.ForeignKey(Skin, models.CASCADE)

    class Meta:
        db_table = 'user_storage_skin'


# class UserProfileManager(BaseUserManager):
#     def create_user(self, phone_number, password=None, **extra_fields):
#         pass
#
#     def create_superuser(self, phone_number, password=None, **extra_fields):
#         pass
#
#
# class UserProfile(AbstractBaseUser):
#     name = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
#     created_at = models.DateField(blank=True, null=True)
#     balance = models.IntegerField(blank=True, null=True)
#
#     objects = UserProfileManager()
#
#     USERNAME_FIELD = 'phone_number'
#
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         db_table = 'user_table'


class UserProfile(models.Model):
    name = models.CharField(max_length=200, default="user")
    phone_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(blank=True, null=True, default=1000)

    class Meta:
        db_table = 'user_table'


class Admin(models.Model):
    # user = models.ForeignKey('UserProfile', models.SET_NULL, blank=True, null=True)
    login = models.CharField(max_length=200, unique=True, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = 'admin'


class AuthenticationCode(models.Model):
    phone_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"Код для {self.phone_number}"
