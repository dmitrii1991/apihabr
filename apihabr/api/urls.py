from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from api.views import launch, get_article, get_articles_by_date, TaskViewSet, ArticleViewSet


router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'articles', ArticleViewSet)


urlpatterns = [
    url(r'^post/$', launch),
    url(r'^article/$', get_article),
    url(r'^articlesbydate/$', get_articles_by_date),
    path('', include(router.urls)),
]