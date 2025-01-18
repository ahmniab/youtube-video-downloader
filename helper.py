import yt_dlp
import json

def get_settings():
    with open('settings.json', 'r') as file:
        return json.load(file)

class LinkError(Exception):
    pass

