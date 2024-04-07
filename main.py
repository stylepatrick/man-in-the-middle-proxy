import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import requests


# http://python.vic-tim.de/images/
# http://python.vic-tim.de/proxy/form.html

class MyHandler(BaseHTTPRequestHandler):
    # replace images with fake images and manipulate title of webpage
    def do_GET(self):
        print("Path: " + self.path)

        if self.path[-4:] == ".jpg":
            self.send_response(200)
            self.send_header("content-type", "image/jpeg")
            self.end_headers()

            with open("cat.jpg", "rb") as img:
                self.wfile.write(img.read())

        else:
            with requests.get(self.path, stream=True) as res:
                print(res.headers["Content-Type"])
                if "text/html" in res.headers["Content-Type"]:
                    self.send_response(res.status_code)
                    self.send_header("content-type", "text/html")
                    self.end_headers()
                    content = str(res.content, "utf-8")
                    content = content.replace("Bilder", "Katzen")
                    self.wfile.write(content.encode())
                else:
                    self.send_response(res.status_code)
                    for key, value in self.headers.items():
                        self.send_header(key, value)
                    self.end_headers()

                    self.wfile.write(res.raw.read())

    # Methode will proxy the POST requests
    # if the form is filled with the message top
    # it will be replaced with flop and send to the server
    # Original received response from server is changed
    # that client will never now that top has changed to flop
    def do_POST(self):
        print(self.path)
        print(self.headers)
        print(self.headers["content-type"])
        if self.headers["content-type"] == "application/x-www-form-urlencoded":
            length = int(self.headers["content-length"])
            form = str(self.rfile.read(length), "utf-8")
            data = urllib.parse.parse_qs(form)

            if "content" in data:
                if type(data["content"]) == list:
                    if len(data["content"]) == 1:
                        data["content"][0] = data["content"][0].replace("top", "flop")

            with requests.post(self.path, data=data, stream=True) as res:
                self.send_response(res.status_code)
                self.send_header("content-type", "text/html")
                self.end_headers()
                print(res.content)
                content = str(res.content, "utf-8")
                # Change back to original value so client will never now
                # that the message was manipulated by the proxy
                content.replace("flop", "top")
                print(self.headers)
                self.wfile.write(content.encode())


class ThreadingHTTPMixing(ThreadingMixIn, HTTPServer):
    pass


address = ("127.0.0.1", 10080)
server = HTTPServer(address, MyHandler)
server.serve_forever()
