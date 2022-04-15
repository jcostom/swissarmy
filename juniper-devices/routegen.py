#!/usr/bin/env python3

"""
All of these routes will be generated in 10/8 with
(by default) a gateway of 10.255.255.254.

There's room down below to grow if anyone would care to
contribute syntax to other router platforms. Just modify
the parser --rtr bit, then add an elif clause for another
flavor of router and send me a pull request.
"""

import argparse
from random import randint

parser = argparse.ArgumentParser(
    prog='routegen.py',
    description='Generate static route statements to load into a router for PoC Testing.'  # noqa: E501
)

parser.add_argument('--count', type=int, default=100, action='store',
                    help="How many routes to generate.")
parser.add_argument('--rtr', default='juniper', action='store',
                    help="Router type: [juniper|cisco], default is juniper.")
parser.add_argument('--gw', action='store', default='10.255.255.254',
                    help="Gateway for routes generated, default is 10.255.255.254.")  # noqa: E501
args = parser.parse_args()


def main():
    for i in range(args.count):
        ip = ".".join(
            ['10', str(randint(0, 255)), str(randint(0, 255)), str(randint(0, 255))]  # noqa: E501
        )
        if args.rtr == 'juniper':
            print(f"set routing-options static route {ip}/32 {args.gw}")
        elif args.rtr == 'cisco':
            print(f"ip route {ip} 255.255.255.255 {args.gw}")
        else:
            print(f"Invalid Router type selected: {args.rtr}.")
            break


if __name__ == "__main__":
    main()
