from django.db import models

class Channel(models.Model):
    tvg_id = models.CharField(max_length=512, blank=True)
    channel_name = models.CharField(max_length=512)
    channel_url = models.URLField()
    channel_logo_url = models.URLField(blank=True, null=True, max_length=1024)
    channel_group = models.CharField(max_length=512, blank=True)
    channel_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.channel_name

class ProgramGuide(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='programguides')
    title = models.CharField(max_length=512)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"
