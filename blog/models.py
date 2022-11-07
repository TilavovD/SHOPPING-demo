from django.db import models


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    summmary = models.CharField(max_length=256)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
