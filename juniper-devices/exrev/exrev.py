#!/usr/bin/env python3

"""
Need to track down the HW revisions of a bunch of EX
switches all at once? This is the place to be.

Run this as:
./exrev.py --config myconfig-file.json \
    --user myuser --password mypassword

Optionally, if you're authenticating via SSH key,
you can leave out the password. If your current username
is the same locally as well as on the switches, you can
leave that out as well!

The only non-default module here is PyEZ. Installation
directions for the module found here:
https://github.com/Juniper/py-junos-eznc
"""

import argparse
import json
import logging
import os
import re
from jnpr.junos import Device

# Setup logger
LOG_LEVEL = 'ERROR'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(asctime)s] %(message)s')
logger = logging.getLogger()

# Setup CLI options
parser = argparse.ArgumentParser(
    description='Find Juniper Switch HW Revisions'
)
parser.add_argument('--config', action="store",
                    default='./config.json',
                    help="Defaults to ./config.json")
parser.add_argument('--user', action="store",
                    default=os.getenv('USER'),
                    help="Will default to your current username.")
parser.add_argument('--password',
                    action="store",
                    help="Omit this option if you're using ssh keys to authenticate")  # noqa E501
args = parser.parse_args()

# Read in configuration
with open(args.config, 'r') as f:
    myconfig = json.load(f)

for switch in myconfig['switches']:
    logger.error(f'Switch: {switch}')
    with Device(host=switch, user=args.user, password=args.password) as jdev:
        res = jdev.cli('show chassis hardware', warning='False')
        members = re.findall(r'^FPC.*', res, re.MULTILINE)
        for member in members:
            print(member)
        print("-----------------------------------------------------------\n")
