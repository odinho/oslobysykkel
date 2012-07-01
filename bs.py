#!/usr/bin/env python3

import time

import oslobysykkel

def format_bargraph(bikes, locks):
    return "\033[44m" + " " * bikes + "\033[47m" + " " * locks + "\033[0m"

if __name__ == "__main__":
    import argparse
    import sys

    """
    sys.stdout.write("%d" % time.time())
    for i in range(oslobysykkel.last_rack):
        try:
            r = oslobysykkel.get_rack(i)
        except IndexError:
            sys.stdout.write(" %d" % -1)
            continue

        sys.stdout.write(" %d" % r.bikes)

    sys.stdout.write("\n")

    exit(0)
    rack_id = int(sys.argv[1])

    for rack_id in range(120):
        try:
            r = oslobysykkel.get_rack(rack_id)
        except IndexError:
            sys.stderr.write("No such rack: %d\n" % rack_id)
            continue
            exit(1)

        print(r)
    """
    rack_id = int(sys.argv[1])
    r = oslobysykkel.get_rack(rack_id)
    print(r.description)
    print(format_bargraph(r.bikes, r.locks))
