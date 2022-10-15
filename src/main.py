import asyncio
import uvloop

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


from config import web_server as server_config
from handler.api import search, post_data, get_status
from src.application.convertor import Convertor
from src.application.noise_removal import NoiseRemoval
from src.application.ocr import OCR
from src.application.finalizer import Finalizer
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from urllib.parse import urlparse, parse_qs
import json


# class HandleRequests(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#     def do_GET(self):
#         self._set_headers()
#         parsed_url = urlparse(self.path)
#
#         parsed = parse_qs(parsed_url.query)
#         print(parsed_url)
#         result = ""
#         if self.path.__contains__('search'):
#             result = search(parsed["key"])
#
#         if self.path.__contains__('get_status'):
#             result = get_status(parsed["key"])
#
#         self.wfile.write(json.dumps(result))
#
#     def do_POST(self):
#         '''Reads post request body'''
#         self._set_headers()
#         content_len = int(self.headers.getheader('content-length', 0))
#         post_body = self.rfile.read(content_len)
#         self.wfile.write("received post request:<br>{}".format(post_body))
#
#     def do_PUT(self):
#         self.do_POST()


# HTTPServer((server_config.HOST, server_config.PORT), HandleRequests).serve_forever()

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))

    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))

        # add a property to the object, just to mess with data
        message['received'] = 'ok'

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))


# async def run(server_class=HTTPServer, handler_class=Server, port=8008):
#     convertor_obj = Convertor("convertor")
#     noise_removal = NoiseRemoval("noise")
#     ocr = OCR("ocr")
#     finalizer = Finalizer("finalizer")
#
#     await convertor_obj.run()
#     await noise_removal.run()
#     await ocr.run()
#     await finalizer.run()
#
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#
#     print('Starting httpd on port %d...' % port)
#     # httpd.serve_forever()
#
#
# if __name__ == '__main__':
#     event_loop = asyncio.get_event_loop()
#     event_loop.run_until_complete(run())
#     event_loop.run_forever()


async def run():
    while True:
        convertor_obj = Convertor("convertor")
        noise_removal = NoiseRemoval("noise")
        ocr = OCR("ocr")
        finalizer = Finalizer("finalizer")

        await convertor_obj.run()
        await noise_removal.run()
        await ocr.run()
        await finalizer.run()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run())
