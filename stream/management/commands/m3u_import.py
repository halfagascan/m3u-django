import re
import requests
from django.core.management.base import BaseCommand
from stream.models import Channel

class Command(BaseCommand):
    help = "Import M3U playlist and populate Channel table."

    def handle(self, *args, **options):
        # Update this with your real playlist URL
        from django.conf import settings
        M3U_URL = getattr(settings, 'M3U_URL', None)
        if not M3U_URL:
            self.stderr.write("Set M3U_URL in your settings or local_settings.py")
            return

        self.stdout.write(f"Downloading playlist from: {M3U_URL}")
        resp = requests.get(M3U_URL)
        if resp.status_code != 200:
            self.stderr.write(f"Failed to download playlist: HTTP {resp.status_code}")
            return

        lines = resp.text.splitlines()
        # Regex for #EXTINF line
        pattern = re.compile(
            r'#EXTINF:-1.*?tvg-id="(?P<tvg_id>[^"]*)".*?tvg-name="(?P<tvg_name>[^"]*)".*?tvg-logo="(?P<tvg_logo>[^"]*)".*?group-title="(?P<group>[^"]*)",(.*)'
        )

        count = 0
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#EXTINF"):
                m = pattern.match(line)
                if m:
                    tvg_id = m.group('tvg_id')
                    tvg_name = m.group('tvg_name')
                    tvg_logo = m.group('tvg_logo')
                    group = m.group('group')
                    # The channel name after the comma, if you want
                    if ',' in line:
                        channel_name = line.split(',', 1)[1]
                    else:
                        channel_name = tvg_name

                    # Next line should be the stream URL
                    url = ""
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith("#"):
                            url = next_line

                    # Load regex patterns from local_settings.py, or allow all if not set
                    TVG_ID_PAT = getattr(settings, 'TVG_ID', r'.*')
                    TVG_NAME_PAT = getattr(settings, 'TVG_NAME', r'.*')
                    TVG_LOGO_PAT = getattr(settings, 'TVG_LOGO', r'.*')

                    # For group filtering with multiple possible allowed groups
                    GROUP_TITLES = getattr(settings, 'GROUP_TITLES', None)
                    if GROUP_TITLES is None:
                        GROUP_TITLE_PAT = getattr(settings, 'GROUP_TITLE', r'.*')
                        group_pass = True if re.fullmatch(GROUP_TITLE_PAT, group) else False
                    else:
                        group_pass = any(re.fullmatch(pattern, group) for pattern in GROUP_TITLES)

                    # Apply all filters
                    if (not re.fullmatch(TVG_ID_PAT, tvg_id)
                        or not re.fullmatch(TVG_NAME_PAT, tvg_name)
                        or not re.fullmatch(TVG_LOGO_PAT, tvg_logo)
                        or not group_pass):
                        continue  # Skip this channel if any filter doesn't match

                    # If we reach here, the channel passes all filters

                    # Create or update channel
                    ch, created = Channel.objects.update_or_create(
                        channel_name=channel_name,
                        defaults={
                            'tvg_id': tvg_id,
                            'channel_logo_url': tvg_logo,
                            'channel_url': url,
                            'channel_group': group,
                            'channel_enabled': True,
                        }
                    )
                    msg = "Created" if created else "Updated"
                    self.stdout.write(f"{msg} channel: {channel_name} [{url}]")
                    count += 1
                else:
                    self.stderr.write(f"NO MATCH for line: {line}")
            i += 1

        self.stdout.write(self.style.SUCCESS(f"Import completed: {count} channels processed."))
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
