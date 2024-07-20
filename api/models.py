from django.db import models

# Create your models here.


class Highlight(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HighlightDetails(models.Model):
    report_id = models.CharField(max_length=255)
    type = models.ForeignKey(Highlight, on_delete=models.CASCADE)
    fight_id = models.IntegerField()
    player_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    img = models.CharField(max_length=255)

    def __str__(self):
        return self.title