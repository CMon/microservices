#!/usr/bin/env python
import argparse
import os
from Configuration import Configuration
from WebApp import WebApp

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--configFile", help="path to configFile", default="~/.config/microservices/authService.yml")
args = parser.parse_args()

config = Configuration(os.path.expanduser(args.configFile))
database = Database(config.getSection("database"))
webserver = WebApp(config.getSection("webServer"), database)