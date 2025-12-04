#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from stream.models import Channel
from urllib.request import urlopen
from django.conf import settings
import re

class Command(BaseCommand):
    help = 'Imports m3u files into the DB'

    def handle(self, *args, **options):    # <--- everything goes inside here
        filename = settings.M3U_URL
        with urlopen(filename) as f:
            lines = [line.decode('utf-8').strip() for line in f.readlines()]

        i = 1
        while i < len(lines) - 1:
            line1 = lines[i]
            line2 = lines[i + 1]
            print("DEBUG L1:", repr(line1))
            print("DEBUG L2:", repr(line2))
            m = re.search(
                r'^#EXTINF:-1 tvh-chnum="[^"]*" tvg-id="([^"]*)" tvg-name="([^"]*)" tvg-logo="([^"]*)" group-title="([^"]*)",(.*)$',
                line1
            )
            url = re.search(r'^(https?://.*)$', line2)
            print("DEBUG m match:", m)
            print("DEBUG url match:", url)
            if m and url:
                print("Inserting:", m.group(5))
                Channel.objects.create(
                    tvg_id=m.group(1),
                    channel_logo_url=m.group(3),
                    channel_group=m.group(4),
                    channel_name=m.group(5),
                    channel_url=url.group(1),
                    channel_enabled=False
                )
            i += 2
        print("Done importing channels.")
