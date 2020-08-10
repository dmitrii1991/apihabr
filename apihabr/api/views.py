import logging

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .tasks import сelery_insert_db
from .models import Task, Article
from .serializers import TaskSerializer, ArticleSerializer, ArticleOneSerializer


logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API-set Task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API-set Article
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_article(request):
    """
    get single article by pk
    """
    pk = request.data.get("pk", 0)
    if article := Article.objects.filter(pk=int(pk)).first():
        serializer = ArticleSerializer(article, many=False)
        logger.info(f'Get {article.title}')
        return Response({"article": serializer.data}, status=status.HTTP_200_OK)
    logger.info(f'Get wrong pk {pk}')
    return Response({"article": "a non-existent value - pk"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_articles_by_date(request):
    """
    get a group of articles by date
    """
    date = request.data.get("date", '01-01-0000')
    if task := Task.objects.filter(date=date, done=True).first():
        articles = Article.objects.filter(id_article=task)
        serializer = ArticleOneSerializer(articles, many=True)
        logger.info(f'Get articles by {task.date}')
        return Response({"articles": serializer.data}, status=status.HTTP_200_OK)
    logger.info(f'Get wrong task.date  {date}')
    return Response({"article": "a non-existent value - date"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@permission_classes((permissions.AllowAny,))
def launch(request):
    """
    manual launch for parsing. ONLY FOR TEST! CELERY MUST WORK!
    """
    logger.warning(f'manual launch for parsing!')
    сelery_insert_db.delay()
    return Response({"response": "parser is working"}, status=status.HTTP_200_OK)