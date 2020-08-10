from rest_framework import serializers

from .models import Task, Article


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = ['date']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Article
        fields = ['pk', 'title', 'url', 'text']


class ArticleOneSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    url = serializers.URLField()
    text = serializers.CharField(max_length=701)

