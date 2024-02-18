from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import (
    SendVerificationCodeView,
    UserProfileDetailView,
    VerifyCodeView,
    UserProfileListCreateView,
    PetListCreateView,
    PetDetailView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Tamagotchi API",
        default_version='v1',
        contact=openapi.Contact(name='test'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth_code/send/', SendVerificationCodeView.as_view(), name='send_code'),
    path('auth_code/verify/', VerifyCodeView.as_view(), name='verify'),
    path('users/', UserProfileListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserProfileDetailView.as_view(), name='user-detail'),
    path('pets/', PetListCreateView.as_view(), name='pet-list-create'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet-detail'),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
