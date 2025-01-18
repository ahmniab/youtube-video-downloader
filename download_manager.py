import yt_dlp
import json
import helper
import os
import threading
download_id = 0

class download:
    def __init__(self, url, format_id, download_path):
        self.url = url
        self.format_id = format_id
        self.download_path = download_path
        self.dlp_dict = {'total_bytes' : 0}

        global download_id
        self.id = download_id
        download_id += 1
        

    def progress_hook(self, d):
        self.dlp_dict = d
    
    def __str__(self):
        json.dumps(self.dlp_dict)
    def __len__(self):
        return self.dlp_dict['total_bytes']
                
                  
active_downloads = []

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
                if f['ext'] == 'mhtml' or f['format_id'].isdigit() == False:
                    continue

                format_info = {
                    'id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('resolution', 'N/A'),
                    'fps': f.get('fps', 'N/A'),
                    'filesize': f.get('filesize', 'N/A'),
                    'vcodec': f.get('vcodec', 'N/A'),
                    'acodec': f.get('acodec', 'N/A'),
                    'format_note': f.get('format_note', 'N/A'),
                }
                formats_list.append(format_info)
        else:
            raise helper.LinkError("No formats found")

        return {"formats":formats_list, "title":info_dict['title'], "thumbnail":info_dict['thumbnail']}

def video_format_condition(f):
    return f['ext'] != 'webm' and f['filesize'] != 'N/A' and f['vcodec'] != 'none'  

def audio_format_condition(f):
    return f['vcodec'] == 'none' and f['acodec'] != 'none' and f['ext'] != 'mp4' and f['ext'] != 'webm' 

def available_download_formats(url):
    # return list_available_formats(url)
    formats = list_available_formats(url)
    
    aud_formats = list(filter(audio_format_condition, formats['formats']))
    vid_formats = list(filter(video_format_condition, formats['formats']))
    vid_with_aud_formats = []
    for f in vid_formats:
        if f['acodec'] == 'none':
            f['id'] = f'{f['id']}+{aud_formats[0]['id']}'
            f['acodec'] = aud_formats[0]['acodec']
            f['filesize'] = f['filesize']+aud_formats[0]['filesize']
        vid_with_aud_formats.append(f)

    return {
        "title":formats['title'], 
        "thumbnail":formats['thumbnail'], 
        "audio":aud_formats, 
        "video":vid_with_aud_formats
        }


def start_download(dl:download):
    ydl_opts = {
        'format': dl.format_id,    
        'progress_hooks': [dl.progress_hook],
        'outtmpl': f'{dl.download_path}%(uploader)s-%(title)s[%(resolution)s].%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if ydl.download([dl.url]) != 0:
            raise yt_dlp.DownloadError("Download failed")

def download_video_in_format(url, format_id)->int:
    settings = helper.get_settings()
    new_download = download(url, format_id, settings['download_path'])
    threading.Thread(target=start_download, args=(new_download,)).start()
    return new_download.id
    
        
