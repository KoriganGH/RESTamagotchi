from django.contrib import admin
from django.urls import path
from backend import urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += urls.urlpatterns
