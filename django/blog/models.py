from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_data = models.DateTimeField(
        default=timezone.now
    )
    published_data = models.DateTimeField(
        blank=True, null=True
    )

    def publish(self):
        self.published_data = timezone.now()
        self.save()

    def __str__(self):
        return self.title

