from django.contrib import admin
from .models import Channel, ProgramGuide

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_name', 'tvg_id', 'channel_group', 'channel_enabled']
    search_fields = ['channel_name', 'tvg_id']
    ordering = ['channel_name']

@admin.register(ProgramGuide)
class ProgramGuideAdmin(admin.ModelAdmin):
    list_display = ['channel', 'title', 'start_time', 'end_time']
    search_fields = ['title', 'channel__channel_name']
    ordering = ['start_time']
