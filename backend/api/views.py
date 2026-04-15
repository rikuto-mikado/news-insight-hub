from rest_framework import viewsets, filters
from .models import NewsArticle
from .serializers import NewsArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving news articles fetched from external sources.
    Supports list and detail views (read-only).
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "source_name", "content"]
    filterset_fields = ["category"]
