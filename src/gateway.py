from config import web_server as server_config

from handler.api import search, get_status, post_data
from http.server import BaseHTTPRequestHandler, HTTPServer


import cgi
from urllib.parse import urlparse, parse_qs
import json

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print("pass {}".format(dir_path))


class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        parsed_url = urlparse(self.path)

        parsed = parse_qs(parsed_url.query)
        print(parsed_url)
        result = ""
        if self.path.__contains__('search'):
            result = search(parsed["key"])

        if self.path.__contains__('get_status'):
            result = get_status(parsed["key"])
        self._set_headers()
        self.wfile.write(bytes(json.dumps(result), "utf8"))

    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        content_len = int(self.headers["Content-Length"])
        post_body = self.rfile.read(content_len)
        # new_post_body = post_body.decode("utf-8")
        # json_post_body = json.loads(post_body)
        file_key, filename, content_type, full_body = self.pre_post(post_body)
        result = post_data(file_key, filename, full_body)
        self._set_headers()
        self.wfile.write(bytes(json.dumps(result), "utf8"))

    def pre_post(self, body):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        data = body.split(pdict['boundary'])
        key_index = data[1].find(b'name="key"')
        file_key = data[1][key_index:].split(b'\r\n')[2].decode('utf8')
        files = data[2].split(b'\r\n\r\n')
        new_files = files[0].split(b'\r\n')
        filename_index = new_files[1].find(b'filename=')
        filename = new_files[1][filename_index:].split(b'=')[1][1:-1].decode('utf8')
        content_type = new_files[2].split(b':')[1].decode('utf8')
        full_body = files[1]
        return file_key, filename, content_type, full_body


HTTPServer((server_config.HOST, server_config.PORT), HandleRequests).serve_forever()
