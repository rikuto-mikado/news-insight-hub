from django.urls import path, include
from rest_framework import routers
from .views import NewsArticleViewSet

routers = routers.DefaultRouter()
routers.register(r"articles", NewsArticleViewSet, basename="newsarticle")

urlpatterns = [path("", include(routers.urls))]
