from django.shortcuts import render
from django.http import HttpResponse
from .models import Channel, ProgramGuide
from django.conf import settings
import bleach
from django.http import HttpResponse

def test_public(request):
    return HttpResponse("It works!")
from .models import Channel, Programmes
from django.conf import settings
import bleach
#CONSTANTS

#M3U AKA CHANNEL LIST
M3U_HEADER = "#EXTM3U"
M3U_LINE_START = "#EXTINF:-1"
M3U_LINE_BREAK = "\n"

#EPG AKA Programme Guides
XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
XML_DOCTYPE = '<!DOCTYPE tv SYSTEM "xmltv.dtd">'
XML_GENERATOR = '<tv generator-info-name="m3udjango 1.0" generator-info-url="https://github.com/markconcept/m3u-django">'
XML_LINE_BREAK = ""
XML_FOOTER = '</tv>'

def logo(request):
    return HttpResponse(return_output)


# M3U Constants
M3U_HEADER = "#EXTM3U"
M3U_LINE_START = "#EXTINF:-1"
M3U_LINE_BREAK = "\n"

# XMLTV (EPG) Constants
XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
XML_DOCTYPE = '<!DOCTYPE tv SYSTEM "xmltv.dtd">'
XML_GENERATOR = '<tv generator-info-name="m3udjango 1.0" generator-info-url="https://github.com/markconcept/m3u-django">'
XML_LINE_BREAK = ""
XML_FOOTER = '</tv>'
def m3u(request):
    channel_list = Channel.objects.all().filter(channel_enabled=True).order_by("epg_id")

    if channel_list:
        # Set the header for the m3u
        output = [M3U_HEADER]

        #Loop through the returned channels and output them
        for channel in channel_list:
            #Formatting for each line

            if channel.channel_logo:
                LOGO_URL = settings.SITE_URL+"/"+str(channel.channel_logo)
            else:
                LOGO_URL = channel.channel_logo_url

            cleaned_Channel = channel.channel_name.strip()

            line = ' tvg-id="{tvg_id}" epg-id="{epg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="{group_title}",{channel_name}'.format(tvg_id=channel.tvg_id,base_url=settings.SITE_URL, tvg_name=cleaned_Channel, tvg_logo=LOGO_URL, epg_id=channel.epg_id, group_title=channel.channel_group, channel_name=channel.channel_name)
            url = channel.channel_url
            #Construct the string
            output.append(M3U_LINE_START+line+M3U_LINE_BREAK+url)

def m3u(request):
    channel_list = Channel.objects.filter(channel_enabled=True).order_by("id")
    output = [M3U_HEADER]

    for channel in channel_list:
        # Compose logo URL
        LOGO_URL = (
            settings.SITE_URL + "/" + str(channel.channel_logo)
            if hasattr(channel, 'channel_logo') and channel.channel_logo
            else channel.channel_logo_url or ""
        )
        cleaned_Channel = channel.channel_name.strip()

        # Don't forget to bleach user-supplied fields
        line = (
            f' tvg-id="{bleach.clean(channel.tvg_id)}" epg-id="{bleach.clean(str(getattr(channel, "epg_id", "")))}"'
            f' tvg-name="{bleach.clean(cleaned_Channel)}" tvg-logo="{bleach.clean(LOGO_URL)}"'
            f' group-title="{bleach.clean(channel.channel_group)}",{bleach.clean(channel.channel_name)}'
        )
        url = channel.channel_url
        output.append(M3U_LINE_START + line + M3U_LINE_BREAK + url)

    return_output = M3U_LINE_BREAK.join(output)
    return HttpResponse(return_output, content_type="application/x-mpegURL")

def epg(request):
    channel_list = Channel.objects.filter(channel_enabled=True).order_by("id")
    programme_list = ProgramGuide.objects.all()

    output = [XML_HEADER, XML_DOCTYPE, XML_GENERATOR]

    # Channels
    for channel in channel_list:
        LOGO_URL = (
            settings.SITE_URL + "/" + str(channel.channel_logo)
            if hasattr(channel, 'channel_logo') and channel.channel_logo
            else channel.channel_logo_url or ""
        )
        cleaned_Channel = channel.channel_name.strip()
        line1 = f'<channel id="{bleach.clean(channel.tvg_id)}">'
        line2 = f'<display-name>{bleach.clean(cleaned_Channel)}</display-name>'
        line3 = f'<icon src="{bleach.clean(LOGO_URL)}"></icon>'
        line4 = f'<lcn>{bleach.clean(str(getattr(channel, "epg_id", "")))}</lcn>'
        line5 = '</channel>'
        output.append(line1 + line2 + line3 + line4 + line5)

    # Programmes
    for programme in programme_list:
        # Get tvg_id from FK channel table
        channel_tvg_id = bleach.clean(getattr(programme.channel, 'tvg_id', ""))
        # Format times
        start_str = programme.start_time.strftime("%Y%m%d%H%M%S %z").strip()
        end_str = programme.end_time.strftime("%Y%m%d%H%M%S %z").strip()
        title = bleach.clean(programme.title)
        desc = bleach.clean(programme.description or "")
        pline1 = f'<programme start="{start_str}" stop="{end_str}" channel="{channel_tvg_id}">'
        pline2 = f'<title>{title}</title>'
        pline3 = f'<desc>{desc}</desc>'
        pline4 = '</programme>'
        output.append(pline1 + pline2 + pline3 + pline4)

    return HttpResponse(return_output)

def epg(request):

    #Load the EPG & Channel List into arrays
    channel_list = Channel.objects.all().filter(channel_enabled=True).order_by("epg_id")
    programme_list = Programmes.objects.all()

    if channel_list:
        # Set the header for the m3u
        output = [XML_HEADER,XML_DOCTYPE,XML_GENERATOR]

        #Loop through the returned channels and output them
        for channel in channel_list:

            if channel.channel_logo:
                LOGO_URL = settings.SITE_URL+"/"+str(channel.channel_logo)
            else:
                LOGO_URL = channel.channel_logo_url

            cleaned_Channel = channel.channel_name.strip()
            #Formatting for each line
            line1 = '<channel id="{tvg_id}">'.format(tvg_id=bleach.clean(channel.tvg_id))
            line2 = '<display-name>{channel_name}</display-name>'.format(channel_name=bleach.clean(cleaned_Channel))
            line3 = '<icon src="{channel_logo}"></icon>'.format(channel_logo=LOGO_URL)
            line4 = '<lcn>{epg_id}</lcn>'.format(epg_id=channel.epg_id)
            line5 = '</channel>'

            #Input these into the array for later on.
            output.append(line1+line2+line3+line4+line5)
    else:
        #Default output if the array is returned null.
        output = "Error: No Enabled Channels Found."

    if programme_list:
            for programme in programme_list:
                #Loop through each programme that's been loaded in.
                pline1 = '<programme start="{start}" stop="{stop}" channel="{tvg_id}">'.format(start=programme.Start, stop=programme.Stop, tvg_id=bleach.clean(programme.Channel))
                pline2 = '<title>{programme_title}</title>'.format(programme_title=programme.Title)
                pline3 = '<desc>{programme_desc}</desc>'.format(programme_desc=programme.Description)
                pline4 = '</programme>'
                #Input these programmes into the array
                output.append(pline1+pline2+pline3+pline4)
    else:
        #Default output if the array is returned null.
        output = "Error: No Programmes Found."

    output.append(XML_FOOTER)
    return_output = XML_LINE_BREAK.join(output)

    return HttpResponse(return_output, content_type="application/xml")
