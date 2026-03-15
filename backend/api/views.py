from rest_framework import viewssets
from .models import NewsArticle
from .serializers import NewsArticleSerializer


# Create your views here.
class NewsArticleViewSet(viewssets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving news articles fetched from external sources.
    Supports list and detail views (read-only).
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
