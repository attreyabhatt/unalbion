from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # This will store Quill HTML
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
