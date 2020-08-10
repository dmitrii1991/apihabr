import logging
import time
from re import search, M
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from .models import Article, Task


logger = logging.getLogger(__name__)


def get_html(url: str) -> "str, str":
    """
    gets url returns HtmlText, status,
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f'Error status:{response.status_code} url:{url}')
            return None, str(response.status_code)
        return response.text, '200'
    except requests.exceptions.ConnectionError:
        logger.error('the connection was broken')
        return None, 'the connection was broken'


def insert_db(url: str = 'https://habr.com/ru/top/') -> None:
    """
    parses the Habr and inserts values in the database
    """

    date_task = timezone.localtime(timezone.now())
    task, created = Task.objects.get_or_create(date=date_task.date())
    if not created:
        if task.done:
            return

    html_resources, status = get_html(url)
    if status == '200':
        soup = BeautifulSoup(html_resources, "html.parser")
        pages = len(soup.find_all(class_="toggle-menu__item_pagination"))
    else:
        logger.error('task was broken')
        return

    for page in range(1, 1 + pages):
        if page == 1:
            articles = soup.find_all(class_="post_preview")
        else:
            html_resources, status = get_html(urljoin(url, f'page{page}/'))
            if status == '200':
                soup = BeautifulSoup(html_resources, "html.parser")
                articles = soup.find_all(class_="post_preview")
            else:
                logger.error('task was broken')
                return

        for i, article in enumerate(articles):
            if processed_article := article.find('a', {'class': 'post__title_link'}):
                title = processed_article.text
                link = processed_article.get('href')
                html_resource_art, status = get_html(link)
            elif processed_article := article.find('a', {'class': 'preview-data__title-link'}):
                title = processed_article.text
                link = processed_article.get('href')
                html_resource_art, status = get_html(link)
            else:
                logger.warning(f'we have problem with {url} - №{i+1} article')
                continue

            soup_article = BeautifulSoup(html_resource_art, "html.parser")
            if paragraph := soup_article.find(class_='post__text'):
                if paragraphs := paragraph.find_all('p'):
                    text = "".join([p.text for p in paragraphs])[:701]
                else:
                    text = paragraph.text[:701].replace('\n', '')
            else:
                text = soup_article.text[:701].replace('\n', '')

            if title and link and text:
                id_post = search('(\d){5,}', link, flags=M).group()
                _, created = Article.objects.get_or_create(id=int(id_post), id_task=task, title=title, url=link, text=text)
                if created:
                    logger.info(f'Find title: {title} link:{link} len_text:{len(text)}')
                else:
                    logger.info(f'title exist!: {title} link:{link} len_text:{len(text)}')
            else:
                logger.error(f'Not find title: {title} link:{link} len_text:{len(text)}')
            # don't get blocked
            time.sleep(0.5)
        task.done = True
        task.save()

