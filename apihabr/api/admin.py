from django.contrib import admin
from.models import Article, Task


@admin.register(Article)
class ArticlePanel(admin.ModelAdmin):
    list_display = ('title', 'url', 'text')


@admin.register(Task)
class TaskPanel(admin.ModelAdmin):
    list_display = ('id', 'date', 'done')
