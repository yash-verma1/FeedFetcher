from django.db import models

class Episode(models.Model):
    podcast_title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField(max_length=200)
    image = models.URLField(max_length=200)
    podcast_name = models.CharField(max_length=100)
    podcast_network = models.CharField(max_length=150)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.podcast_title}"
    
