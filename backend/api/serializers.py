from rest_framework import serializers
from .models import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "content",
            "url",
            "source_name",
            "author",
            "published_date",
        ]
