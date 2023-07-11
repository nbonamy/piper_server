#!/usr/bin/env python3

from src.utils import *
from src.configuration import Configuration
from src.http_server import HttpServer
from src.synthesizer import Synthesizer
from threading import Event

def main():

  # load config
  config = Configuration(load_yaml('config/config.yml'))

  # synthetizer
  synthesizer = Synthesizer(config)

  # http server
  server = HttpServer(config, lambda text, voice: synthesizer.synthesize(text, voice))
  server.start()

  # wait for ctrl-c
  Event().wait()

if __name__ == '__main__':
  main()
