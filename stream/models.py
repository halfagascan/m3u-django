from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

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

class Channel(models.Model):
    id = models.AutoField(primary_key = True)
    tvg_id = models.CharField(max_length=999)
    epg_id = models.BigIntegerField(default=9999)
    channel_group = models.CharField(max_length=200)
    channel_name = models.CharField(max_length=200)
    channel_url = models.CharField(max_length=1200)
    channel_logo = models.ImageField(upload_to='channel_logos/', null=True, blank=True)
    channel_logo_url = models.URLField(max_length=1200, null=True, blank=True)
    channel_enabled = models.BooleanField(default=False)
    channel_protected = models.BooleanField(default=False)
    stream_active = models.BooleanField(default=True)

class Programmes(models.Model):
    Start = models.CharField(max_length=400)
    Stop = models.CharField(max_length=400)
    Channel = models.CharField(max_length=400)
    Title = models.CharField(max_length=400)
    Description = models.CharField(max_length=99999, null=True)

class EPGChannels(models.Model):
    ChannelName = models.CharField(max_length=400, primary_key=True)
