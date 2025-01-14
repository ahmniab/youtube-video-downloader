from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import helper

class HTTPRequestHandler(BaseHTTPRequestHandler):

    # Handle GET requests
    def do_GET(self):
        print('path '+self.path)
        if self.path == "/":
            self.serve_file("appui/index.html", "text/html")
        elif self.path == "/setting" or self.path == "/settings":
            self.serve_file("appui/setting.html", "text/html")

        elif self.path.startswith("/css"):
            self.serve_file(f"appui{self.path}", "text/css")
        elif self.path.startswith("/js"):
            self.serve_file(f"appui{self.path}", "application/javascript")
        else:
            self.handle_not_found()

    # Handle POST requests
    def do_POST(self):
        if self.path == "/vid-info":
            self.handle_vid_info()
        else:
            self.handle_not_found()



    # Submit endpoint (handles POST data)
    def handle_vid_info(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
            print("Received data:", data)
            if "link" not in data and not isinstance(data["link"], str):
                raise ValueError("Invalid data format")
            
            downloads = helper.available_downloads(data["link"])
            
            # everything is fine
            self.send_json_data(downloads)

        except json.JSONDecodeError:
            self.handle_client_error("Invalid JSON")
        except ValueError:
            self.handle_client_error("Invalid data format")
        except helper.LinkError :
            self.handle_client_error(formats["error"])


    
    #helping functions
    def handle_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"404 - Page not found")
    
    def handle_client_error(self, error_message):
        self.send_response(400)
        self.send_header("Content-type", "text/html")
        response = {"error": error_message}
        self.wfile.write(json.dumps(response).encode("utf-8"))
    def send_json_data(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
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
