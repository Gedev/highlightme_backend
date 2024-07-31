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


class CREATION_STATUS(models.TextChoices):
    CREATED = "CREATED", "Created"
    FAILED = "FAILED", "Failed"
    REFUSED = "REFUSED", "Refused"


class HighlightLogs(models.Model):
    report_owner = models.CharField(max_length=255)
    realm = models.CharField(max_length=255)
    highlight_type = models.CharField(max_length=255)
    guild_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    creation_status = models.CharField(max_length=20, choices=CREATION_STATUS.choices)

    def __str__(self):
        return f"{self.report_owner} - {self.highlight_type} - {self.timestamp}"
