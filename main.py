from http.server import HTTPServer
from request_handler import HTTPRequestHandler
import helper
import webbrowser

# Run the server
if __name__ == "__main__":

    settings = helper.get_settings()
    server_address = ("", settings["port"])
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    server_url = f'http://localhost:{settings["port"]}'
    print(f"Server running on {server_url}")
    webbrowser.open_new_tab(server_url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass