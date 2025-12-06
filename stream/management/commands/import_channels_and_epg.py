import m3u8
import xmltv
from django.core.management.base import BaseCommand
from stream.models import Channel, ProgramGuide  # Adapt if you have a guide model

class Command(BaseCommand):
    help = "Import channels from M3U8 and EPG from XMLTV"

    def add_arguments(self, parser):
        parser.add_argument("--playlist", type=str, required=True, help="Path or URL to .m3u or .m3u8 file")
        parser.add_argument("--epg", type=str, required=False, help="Path to XMLTV EPG file")

    def handle(self, *args, **options):
        playlist_source = options["playlist"]
        epg_path = options.get("epg")

        # --- M3U8 importing (channels only, simple EXTINF/URL pairs) ---
        print(f"Loading playlist: {playlist_source} ...")
        playlist = m3u8.load(playlist_source)

        # m3u8 library is most robust for HLS segments, but for EXTINF pairs, we also need manual scanning for channel attributes.
        # Fallback: if EXTINF attributes aren't exposed, use manual file read for channel info.

        imported_channels = 0
        with open(playlist_source, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            i = 0
            while i < len(lines) - 1:
                extinf_line = lines[i]
                url_line = lines[i + 1]
                if extinf_line.startswith("#EXTINF:") and url_line.startswith("http"):
                    # Channel info parsing (using regex, can improve for m3u8)
                    import re
                    m = re.search(
                        r'^#EXTINF:-1.*?tvg-id="([^"]*)".*?tvg-name="([^"]*)".*?tvg-logo="([^"]*)".*?group-title="([^"]*)",(.*)$',
                        extinf_line
                    )
                    if m:
                        Channel.objects.get_or_create(
                            tvg_id=m.group(1),
                            channel_logo_url=m.group(3),
                            channel_group=m.group(4),
                            channel_name=m.group(5),
                            defaults={
                                "channel_url": url_line,
                                "channel_enabled": False,
                            },
                        )
                        imported_channels += 1
                    i += 2
                else:
                    i += 1
        print(f"Imported {imported_channels} channels from M3U/M3U8.")

        # --- XMLTV importing (EPG) ---
        if epg_path:
            print(f"Loading EPG: {epg_path} ...")
            epg = xmltv.parse(epg_path)
            guide_count = 0
            # Example ProgramGuide import loop (adapt field names to your model!)
            for prog in epg["programmes"]:
                # Attempt to link to your Channel by tvg_id or channel_name
                tvg_id = prog.get("channel")
                title = prog.get("title", [""])[0]
                start = prog.get("start")
                stop = prog.get("stop")
                desc = prog.get("desc", [""])[0] if "desc" in prog else ""
                channel_obj = Channel.objects.filter(tvg_id=tvg_id).first()
                # Only import if the channel exists
                if channel_obj and hasattr(channel_obj, "programguide_set"):
                    channel_obj.programguide_set.create(
                        title=title,
                        start_time=start,
                        end_time=stop,
                        description=desc,
                    )
                    guide_count += 1
            print(f"Imported {guide_count} programs from XMLTV EPG.")

        print("Done!")
