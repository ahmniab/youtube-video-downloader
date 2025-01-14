import yt_dlp
import json

def get_settings():
    with open('settings.json', 'r') as file:
        return json.load(file)

class LinkError(Exception):
    pass

def list_available_formats(url):
    ydl_opts = {
        'quiet': True,  
        'extract_flat': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        formats_list = []

        if 'formats' in info_dict:
            for f in info_dict['formats']:
                format_info = {
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('resolution', 'N/A'),
                    'fps': f.get('fps', 'N/A'),
                    'filesize': f.get('filesize', 'N/A'),
                    'vcodec': f.get('vcodec', 'N/A'),
                    'acodec': f.get('acodec', 'N/A'),
                }
                formats_list.append(format_info)
        else:
            return {'error': 'No formats found.'}

        return formats_list

def video_format_condition(f):
    return f['ext'] != 'mhtml' and f['ext'] != 'webm' and f['filesize'] != 'N/A' and (f['vcodec'] != 'none' and f['fps'] >= 25) and int(f['id']) < 300

def audio_format_condition(f):
    return f['vcodec'] == 'none' and f['acodec'] != 'none' and f['ext'] != 'mp4' and f['ext'] != 'webm' and len(f['id']) < 4

def available_downloads(url):
    formats = list_available_formats(url)
    if 'error' in formats:
        raise LinkError(formats['error'])
    
    aud_formats = list(filter(audio_format_condition, formats))
    vid_formats = list(filter(video_format_condition, formats))
    vid_with_aud_formats = []
    for f in vid_formats:
        if f['acodec'] == 'none':
            f['id'] = f'{f['id']}+{aud_formats[0]['id']}'
            f['acodec'] = aud_formats[0]['acodec']
        vid_with_aud_formats.append(f)

    return {"audio":aud_formats,"video":vid_with_aud_formats}



def download_video_in_format(url, format_id):
    settings = get_settings()
    ydl_opts = {
        'format': format_id,  
        'outtmpl': f'{settings['download_path']}%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])