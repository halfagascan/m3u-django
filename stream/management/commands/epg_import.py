#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from stream.models import Channel, ProgramGuide
from urllib.request import urlopen
from django.conf import settings
from datetime import datetime
import xmltodict
import bleach

def insert_show(START, STOP, CHANNEL_TVG_ID, TITLE, DESC):
    try:
        # Parse datetime fields (expect 'YYYYMMDDhhmmss ±zzzz')
        try:
            start_dt = datetime.strptime(START[:14], "%Y%m%d%H%M%S")
        except Exception as e:
            print(f"[!] Invalid start: {START} for show {TITLE}, skipping")
            return
        try:
            stop_dt = datetime.strptime(STOP[:14], "%Y%m%d%H%M%S")
        except Exception:
            stop_dt = start_dt  # fallback

        # Find enabled Channel matching tvg_id
        channel_obj = Channel.objects.filter(tvg_id=CHANNEL_TVG_ID, channel_enabled=True).first()
        if not channel_obj:
            print(f"Channel {CHANNEL_TVG_ID} not found/enabled. Skipping show: {TITLE}")
            return

        ProgramGuide.objects.create(
            channel=channel_obj,
            title=TITLE,
            start_time=start_dt,
            end_time=stop_dt,
            description=DESC or ""
        )
        print(f"[*] Inserted '{TITLE}' into channel '{channel_obj.channel_name}'")
    except Exception as e:
        print(f"[!] Exception inserting show '{TITLE}': {str(e)}")

class Command(BaseCommand):
    help = 'Imports xml epg files into the DB'

    def handle(self, *args, **options):
        # Check XML_URL setting
        if not getattr(settings, "XML_URL", None):
            print("Update xml URL in settings/config please (XML_URL)")
            return

        try:
            print("Clearing existing EPG program data ...")
            ProgramGuide.objects.all().delete()

            filename = settings.XML_URL
            print(f"Downloading EPG from {filename} ...")
            with urlopen(filename) as file:
                data = file.read()
            print("Parsing EPG XML ...")
            data = xmltodict.parse(data)
            programme_array = data['tv']['programme']
            total = len(programme_array)
            print(f"EPG contains {total} programme entries.")

            inserted = 0
            for i, programme in enumerate(programme_array, 1):
                print(f"Processing {i} of {total}")

                START = programme['@start']
                STOP = programme['@stop']
                CHANNEL = programme['@channel']

                title_field = programme.get('title')
                # handle <title> as dict or str
                if isinstance(title_field, dict) and '#text' in title_field:
                    TITLE = bleach.clean(title_field['#text'])
                elif isinstance(title_field, str):
                    TITLE = bleach.clean(title_field)
                else:
                    TITLE = ""

                desc_field = programme.get('desc')
                if isinstance(desc_field, dict) and '#text' in desc_field:
                    DESC = bleach.clean(desc_field['#text'])
                elif isinstance(desc_field, str):
                    DESC = bleach.clean(desc_field)
                else:
                    DESC = f"{TITLE} on {CHANNEL}"

                # Insert only if Channel exists and is enabled
                before_count = ProgramGuide.objects.count()
                insert_show(START, STOP, CHANNEL, TITLE, DESC)
                after_count = ProgramGuide.objects.count()
                if after_count > before_count:
                    inserted += 1

            print(f"Import complete. {inserted} programmes imported out of {total} in EPG.")

        except Exception as e:
            print(f"[!!] EPG import failed: {str(e)}")
