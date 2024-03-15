from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Tamagotchi test API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'food', FoodViewSet, basename='food')
router.register(r'categories_food', CategoryFoodViewSet, basename='category_food')
router.register(r'personality', PersonalityViewSet, basename='personality')
router.register(r'skin', SkinViewSet, basename='skin')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'games', GameViewSet, basename='game')
router.register(r'user_storage_food', UserStorageFoodViewSet, basename='user_storage_food')
router.register(r'user_storage_skin', UserStorageSkinViewSet, basename='user_storage_skin')
router.register(r'user_profiles', UserProfileViewSet, basename='user_profile')
router.register(r'admins', AdminViewSet, basename='admin')

urlpatterns = [
    path('auth_code/send/', SendVerificationCodeView.as_view(), name='send_code'),
    path('auth_code/verify/', VerifyCodeView.as_view(), name='verify'),
    path('pets/<int:pk>/points/', PetPointsAPIView.as_view(), name='pet_points'),
    path('', include(router.urls)),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
