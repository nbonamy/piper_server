
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus
from threading import Thread

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
  pass

class HttpServer:

  def __init__(self, config, processor):
    self._config = config
    self._processor = processor
    self._server = None

  def delete(self):
    if self._server is not None:
      self._server.shutdown()
      self._server = None

  def start(self):
    port = self._config.get('http_server_port', 5008)
    socketserver.TCPServer.allow_reuse_address = True
    socketserver.TCPServer.allow_reuse_port = True
    self._server = ThreadedTCPServer(('0.0.0.0', port), ApiHandler)
    self._server.processor = self._processor
    self._server_thread = Thread(target=self._server.serve_forever)
    self._server_thread.daemon = True
    self._server_thread.start()
    print(f'API server started at {port}')

class ApiHandler(http.server.BaseHTTPRequestHandler):

  def get_parameters(self):
    query = urlparse(self.path).query
    return dict((k, v[0] if isinstance(v, list) and len(v) == 1 else v)
      for k, v in parse_qs(query).items())

  def do_GET(self):
    if (self.path.startswith('/synthesize')):

      # get parameters
      text = self.get_parameters().get('text')
      voice = self.get_parameters().get('voice')
      print(f'Text to synthetize received: "{text[0:256]}"')

      # start headers
      self.send_response(HTTPStatus.OK)
      self.send_header('Content-type', 'application/octet-stream')
      self.end_headers()

      # now write bytes as they come
      try:
        for bytes in self.server.processor(text, voice):
          self.request.sendall(bytes)
      except:
        pass
      
      # done
      print(f'"{text[0:32]}..." Done!')

  def error(self, code=HTTPStatus.INTERNAL_SERVER_ERROR):
    self.send_response(code)
    self.end_headers()

  def log_message(self, format, *args):
    pass
