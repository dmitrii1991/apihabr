from django.db import models



class Task(models.Model):
    date = models.DateField(db_index=True, verbose_name='дата задания')
    done = models.BooleanField(default=False, verbose_name='выполнено')

    class Meta:
        verbose_name = 'Задача на сбор статей'
        verbose_name_plural = 'Задачи на сбор статей'


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    id_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=256, default='', verbose_name='Заголовок статьи')
    url = models.URLField(verbose_name='url статьи')
    text = models.CharField(max_length=701, default='', verbose_name='700 символов текста статьи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
