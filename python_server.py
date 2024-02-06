import http.server
import socketserver

# Define the port you want to use
port = 3030

# Create a custom request handler to handle redirection
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check the requested path and redirect if necessary
        if self.path == "/web":
            # Redirect to a different URL (e.g., http://example.com)
            self.send_response(302)
            self.send_header("Location", "http://souq-nail-salon.localhost:8080/v2/edit")
            self.end_headers()
        else:
            # Serve other content as usual
            super().do_GET()

# Create the HTTP server
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Serving on port {port}")
    # Start the server
    httpd.serve_forever()
