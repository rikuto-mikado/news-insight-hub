from django.contrib import admin
from .models import NewsArticle


# Register your models here.
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "source_name",
        "published_date",
    )
    search_fields = ("title", "source_name", "author")
    list_filter = ("source_name",)
