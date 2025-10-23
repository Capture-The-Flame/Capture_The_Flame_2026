# flagserver.py
from http.server import BaseHTTPRequestHandler, HTTPServer

FLAG = "flame{unmasked_at_dawn}"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # exact path checks (use tuples or direct equality)
        if self.path == "/" or self.path == "/unmask":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()

            # present a short witty message and the flag for /unmask,
            # otherwise the general welcome for "/"
            if self.path == "/":
                body = (
                    "Welcome to the Masquerade Ball\n\n"
                    "Velvet and varnish hide many hands. A steward signs twice, yet he is only one.\n"
                    "Some names on the rolls are written with a stranger's hand.\n\n"
                    "To those who seek audience: lift the mask and claim what was hidden.\n"
                )
            else:  # /unmask
                body = (
                    "The Mask Falls\n\n"
                    "The steward stands unmasked, and the ledger's forgery is revealed.\n"
                    "A false hand has signed where it should not. The court exhales; a single secret is carried into the light.\n\n"
                    f"Token of exposure: {FLAG}\n"
                )

            self.wfile.write(body.encode("utf-8"))
            return

        # any other path
        self.send_response(404)
        self.end_headers()

    # suppress default logging to keep logs tidy (optional)
    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Flag server listening on :8000")
    server.serve_forever()

