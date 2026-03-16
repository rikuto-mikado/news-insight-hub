import os
import requests
from django.core.management.base import BaseCommand
from api.models import NewsArticle


class Command(BaseCommand):
    help = "Fetch news articles from NewsAPI and save into the database"

    def handle(self, *args, **kwargs):
        api_key = os.environ.get("NEWS_API_KEY")
        if not api_key:
            self.stdout.write(self.style.ERROR("NEWS_API_KEY is not set."))
            return

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        count = 0

        for article in articles:
            # Avoid duplicates by using URL as a unique identifier
            _, created = NewsArticle.objects.get_or_create(
                url=article["url"],
                defaults={
                    "title": article["title"] or "",
                    "content": article.get("content", ""),
                    "source_name": article["source"]["name"],
                    "author": article.get("author", ""),
                    "published_date": article["publishedAt"],
                },
            )
            if created:
                count += 1

        self.stdout.write(f"{len(articles)} articles fetched")
