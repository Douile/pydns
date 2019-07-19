#!/usr/bin/python3

import argparse

import dns
from hosts import parse_hosts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A python DNS server')
    parser.add_argument('-f','--hosts',default='hosts.txt',help='The file to load hosts from')
    parser.add_argument('-a','--address',default='127.0.0.1',help='Address to bind')
    parser.add_argument('-p','--port',default=53,type=int,help='Port to bind')
    parser.add_argument('-d','--debug',action='store_true',default=False,help='Print debug messages')
    args = parser.parse_args()

    defs = parse_hosts(args.hosts)
    if args.debug:
        print(defs)
    server = dns.UDPServer(defs,(args.address,args.port),args.debug)
    server.start()
