# Django M3U Manager

*Edit M3U IPTV stream files using a django panel.*

### Features

- M3U File Import
- EPG File Import
- Produces a filter EPG that includes only the active / enabled channels
- Generates M3U Playlist and EPG

# How to build
1. Clone git to machine that Django will run on `git clone https://github.com/markconcept/m3u-django.git`
2. Update the local settings file with your M3U & EPG URL, renaming the file when done
`mv local_settings.py.sample local_settings.py`
3. Start th container
`docker-compose up`
4. Run migrations
`docker exec -it m3u-django-web-1 python manage.py migrate`
5. Create a admin user
`docker exec -it m3u-django-web-1 python manage.py createsuperuser`
Input a username, email and password,
6. Import M3U
`docker exec -it m3u-django-web-1 python manage.py m3u_import`
'docker exec -it m3u-django-fork-web-1 python manage.py m3u_import'

# Configuring to your requirements

The M3U import script will, by default import any channels from the M3U where the group starts with `UK` or `USA`. This can easily be changed to your requirements.

1. In your local settings change the regex
`vi composeexample/local_settings.py`
2. Change the regex to what you want to filter
`#REGEX FILTERS`
`TVG_ID='.*'`
`TVG_NAME='.*'`
`TVG_LOGO='.*'`
`GROUP_TITLE='UK.*|USA.*'`

Suggestions:
`.*` = all, this should be the default
`UK.*` will match `UK - 123 ABC Channel`

3. Save and close.
`ESC + :wq!`

# Enabling Channels

No programms will be imported by the cron until channels are enabled.
Go into the panel; `http://127.0.0.1:8000` login with your super user details.

1. Go to channels
`http://127.0.0.1:8000/stream/channel/`
2. Select the channels you want to enable, using the drop down select `Enable Channel` then `Go`.
3. EPG for enabled channels will be auto-imported by the cronjob, but you can run the cron manually by running:
`docker exec -it m3u-django-web-1 python manage.py epg_import`
`docker exec -it m3u-django_web_1 python manage.py epg_import`

# URLs

**Admin Panel**
http://127.0.0.1:8000

**Admin Panel - Channels**
http://127.0.0.1:8000/stream/channel/

**M3U Output File**
http://127.0.0.1:8000/channels/

**EPG Ouput File**
http://127.0.0.1:8000/epg/


###End

This fork added: 
    ## Streaming IPTV and EPG Data

This project serves M3U playlists and XMLTV EPG directly from the database via HTTP endpoints, making integration with VLC, TVHeadend, or any IPTV client simple and dynamic.

### 📺 How to connect VLC to the playlist

1. **Import the playlist:**
   - Open VLC.
   - Go to **Media → Open Network Stream**.
   - Enter the playlist URL (for example):  
     ```
     http://<server_ip>:8000/YOUR.m3u
     ```
   - Click **Play**. The channels will appear and stream directly from your server.

2. **Playlist auto-updates:**  
   Channels shown in VLC reflect the current state of your database, including any changes made via the Django admin.

---

### 🖥 How to connect TVHeadend

1. **Add an M3U (IPTV Automatic Network):**
   - In the TVHeadend web interface, go to **Configuration → DVB Inputs → Networks**.
   - Add a new network of type **IPTV Automatic Network**.
   - Set the "Playlist URL" to:
     ```
     http://<server_ip>:8000/YOUR.m3u
     ```

2. **Add an EPG source (XMLTV):**
   - Go to **Configuration → EPG Grabber Modules**.
   - Enable the **XMLTV: Remote** module.
   - Set the XMLTV URL to:
     ```
     http://<server_ip>:8000/epg.xml
     ```
   - TVHeadend will import program guide information directly from your server.


- **Channels and EPG info are managed using the Django admin.**
- Changes are reflected instantly in the output playlists and guides.
- No need to export static files—clients read playlist and guide data directly from HTTP endpoints.



- **M3U Playlist:**  
  `http://<server_ip>:8000/YOUR.m3u`  
  (Replace `<server_ip>` with your actual server address.)

- **XMLTV EPG:**  
  `http://<server_ip>:8000/epg.xml`


### 🔒 Access control

For production use, consider restricting access to these endpoints via authentication or IP whitelisting, especially for public servers.


### Recent Changes

- **Switched to HTTP-served M3U and XMLTV endpoints** (instead of static file exports) for playlist and EPG data.
- **Improved file handling:** Playlists and guides are now dynamically generated from the database, ensuring clients like VLC and TVHeadend always receive up-to-date channel and program information.
- **Simplified client integration:** Endpoints can be consumed directly by IPTV clients, reducing manual file management and eliminating the need to copy/export files for client updates.
- **Channel and EPG admin via Django:** All changes are made via the admin interface and reflected immediately in the output.

Switch endpoints to /YOUR.m3u and /epg.xml for dynamic, always-up-to-date playlist and EPG delivery. Improves file handling and makes client configuration easier.










#### Need help with a client or automation?  
Contact the maintainer or open an issue!














=======
>>>>>>> 835dd6c1bdc14049443767efc134dfedeebcc727
