from http.server import BaseHTTPRequestHandler
import json
import helper
from yt_dlp import DownloadError
import download_manager
import page_builder


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
        self.end_headers()

    # Handle GET requests
    def do_GET(self):
        print('path '+self.path)
        if self.path == "/":
            self.serve_page("index")
        elif self.path == "/setting" or self.path == "/settings":
            self.serve_page("setting") 
        elif self.path == "/change-settings" :
            self.serve_file('settings.json', 'application/json')
        elif self.path == "/downloads":
            self.handle_downloads()

        elif self.path.startswith("/css"):
            self.serve_file(f"appui{self.path}", "text/css")
        elif self.path.startswith("/js"):
            self.serve_file(f"appui{self.path}", "application/javascript")
        elif self.path.startswith("/favicon.ico"):
            self.serve_file(f"appui/images/favicon.ico", "image/x-icon")

        else:
            self.handle_not_found()
        

    # Handle POST requests
    def do_POST(self):
        if self.path == "/vid-info":
            self.handle_vid_info()
        elif self.path == "/change-settings" :
            self.handle_change_settings()
        elif self.path == "/download":
            self.handle_download_request()
        else:
            self.handle_not_found()



    # Submit endpoint (handles POST data)
    def handle_vid_info(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
            print("Received data:", data)
            if ("link" not in data and not isinstance(data["link"], str)):
                raise ValueError
            
            download_formats = download_manager.available_download_formats(data["link"])
            
            # everything is fine
            self.send_json_data(download_formats)

        except json.JSONDecodeError:
            self.handle_client_error("Invalid JSON")
        except ValueError:
            self.handle_client_error("Invalid data format")
        except helper.LinkError :
            self.handle_client_error(download_formats["error"])
        except:
            self.handle_client_error("Unknown error")

    def handle_download_request(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
            print("Received data:", data)
            if "link" not in data and not isinstance(data["link"], str) or \
               "id" not in data and not isinstance(data["format"], str) :
                raise ValueError("Invalid data format")
            
            download_id = download_manager.download_video_in_format(data["link"], data["id"])
            
            # everything is fine
            self.send_json_data({"id": download_id})

        except json.JSONDecodeError:
            self.handle_client_error("Invalid JSON")
        except ValueError:
            self.handle_client_error("Invalid data format")
        except helper.LinkError :
            self.handle_client_error("Invalid link")
        except DownloadError:
            self.handle_client_error("Download failed")
    
    def handle_downloads(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        # self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(download_manager.get_active_downloads()).encode("utf-8"))

    def handle_change_settings(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
            print("Received data:", data)
            if "port" not in data and not isinstance(data["port"], int) or \
               "download_path" not in data and not isinstance(data["download_path"], str) :
                raise ValueError("Invalid data format")
                        
            # everything is fine
            self.save_new_settings(data)
            self.send_json_data({"massage": 'done'})


        except json.JSONDecodeError:
            self.handle_client_error("Invalid JSON")
        except ValueError:
            self.handle_client_error("Invalid data format")
        # except :
        #     print('Unkown Error')

        
        
    
    #helping functions
    def handle_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"404 - Page not found")
    
    def handle_client_error(self, error_message):
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.wfile.write(json.dumps({"error": error_message}).encode("utf-8"))

    def send_json_data(self, data):
        self.send_response(200)
        # self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    
    def serve_file(self, filename, content_type):
        try:
            with open(filename, "rb") as file:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(file.read())

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 - File not found")

    def save_new_settings(self, settings_data:json):
        if settings_data['download_path'][-1] not in '/\\' :
            settings_data['download_path'] += '/'

        with open('appui/js/server_info.js', 'w') as f:
            hostname = f"HOST_NAME = 'localhost:{settings_data['port']}'"
            print(f'new hastname : {hostname}')
            f.write(hostname)

        with open('settings.json', 'w') as f:
            json.dump(settings_data, f)
    
    def serve_page(self, name:str):
        try: 
            page_text = page_builder.get_page(name)
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(page_text, "utf-8"))

        except FileNotFoundError :
            self.handle_not_found()

        
        
