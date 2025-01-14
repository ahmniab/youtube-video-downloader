from http.server import HTTPServer
from request_handler import HTTPRequestHandler
import helper
# Run the server
if __name__ == "__main__":

    settings = helper.get_settings()

    server_address = ("", settings["port"])
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print(f"Server running on http://localhost:{settings["port"]}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass