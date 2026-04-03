from django.db import models


# Create your models here.
class NewsArticle(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True, null=True)
    url = models.URLField(unique=True)
    source_name = models.CharField(max_length=100)
    author = models.CharField(max_length=250, blank=True, null=True)
    published_date = models.DateTimeField()
    category = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]
