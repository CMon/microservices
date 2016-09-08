#!/usr/bin/env python
from pyrabbit.api import Client

import argparse
from pprint import pprint

def getVhosts(cl):
    return cl.get_all_vhosts();

def getQueues(cl, vhost):
    return cl.get_queues(vhost)

parser = argparse.ArgumentParser()
parser.add_argument("--user", help="the user to login", required=True)
parser.add_argument("--password", help="the password to login", required=True)
parser.add_argument("--host", help="the host where rabbitmq runs on", required=True)
parser.add_argument("--port", help="the the port where rabbitmq listens to", default=15672)

parser.add_argument("--listVhosts", help="list available vhosts", action="store_true")
parser.add_argument("--vhost", help="use given vhost")

parser.add_argument("--listQueues", help="list available Queues", action="store_true")
parser.add_argument("--queue", help="use given queue")

parser.add_argument("--message", help="The message to send")
parser.add_argument("--listen", help="wait for a message on that channel", action="store_true")

args = parser.parse_args()

client = Client(args.host + ":" + str(args.port), args.user, args.password)

if args.listVhosts:
    pprint(getVhosts(client))
    exit(0)

if not args.vhost:
    print("vhost argument is needed")
    exit(1)
elif not args.vhost in getVhosts(client):
    print("vhost not available")
    exit(2)


if args.listQueues:
    pprint(getQueues(client, args.vhost))
    exit(0)

if not args.queue:
    print("queue argument is needed")
    exit(1)
elif not args.queue in getQueues(client, args.vhost):
    print("queue does not exist (yet)")
    exit(2)

if args.message:
    print "TODO: send message"

elif args.listen:
    pprint(client.get_messages(args.vhost, args.queue))
