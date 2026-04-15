from celery import shared_task
from django.core.management import call_command

CATEGORIES = ["technology", "business", "sports", "entertainment", "health", "science"]


@shared_task
def fetch_news_task():
    call_command("fetch_news")
    for category in CATEGORIES:
        call_command("fetch_news", category=category)
