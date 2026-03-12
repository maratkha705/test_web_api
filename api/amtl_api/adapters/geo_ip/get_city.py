import argparse
import random
import socket
import struct
import timeit

import geoip2.database
import geoip2.errors

parser = argparse.ArgumentParser(description="Benchmark maxminddb.")
parser.add_argument("--count", default=250000, type=int, help="Number of lookups")
parser.add_argument("--mode", default=0, type=int, help="Reader mode to use")
parser.add_argument("--file", default="GeoLite2-City.mmdb", help="Path to mmdb file")

args = parser.parse_args()
reader = geoip2.database.Reader(args.file, mode=args.mode)


def lookup_ip_address():
    ip = socket.inet_ntoa(struct.pack("!L", random.getrandbits(32)))
    try:
        record = reader.city(str(ip))
        print(f"IP: {ip}; Record: {record}")
    except geoip2.errors.AddressNotFoundError as exc:
        print(f"Error: {exc}")


elapsed = timeit.timeit(
    "lookup_ip_address()",
    setup="from __main__ import lookup_ip_address",
    number=args.count,
)

print("Lookups per second:", args.count / elapsed)
print("Args count:", args.count)
