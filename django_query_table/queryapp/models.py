from django.db import models

class SQLQuery(models.Model):
    name = models.CharField(max_length=255)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
