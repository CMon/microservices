#!/usr/bin/env python
import argparse
import os
from Configuration import Configuration
from WebApp import WebApp
from Database import Database

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--configFile", help="path to configFile", default="~/.config/microservices/authService.yml")
args = parser.parse_args()

config = Configuration(os.path.expanduser(args.configFile))
database = Database(config.getSection("database"))
webserver = WebApp(config.getSection("webServer"), database)

app = webserver.createApp()
app.run(debug=config.getSection("webServer")["debug"], host=config.getSection("webServer")["listenHost"], port=config.getSection("webServer")["listenPort"])
