#!/usr/bin/env python3

"""
We had a customer that needed to find the HW Revisions
for all of their EX switches. This might not be the most
attractive output, but it's pretty reliable. Warning, it
doesn't do a lot of error checking when it connects to
switches, so if soemthing's gone wrong like bad auth
credentials, it will just throw an exception and quit.

The only non-default module here is PyEZ. Installation
directions for the module found here:
https://github.com/Juniper/py-junos-eznc
"""

import argparse
import json
import logging
import re
from jnpr.junos import Device

# Setup logger
logger = logging.getLogger()
ch = logging.StreamHandler()
logger.setLevel(logging.ERROR)
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Setup CLI options
parser = argparse.ArgumentParser(
    description='Find Juniper Switch HW Revisions'
)
parser.add_argument('--config', action="store", default='./config.json', help="Defaults to ./config.json")  # noqa E501
args = parser.parse_args()

# Read in configuration
with open(args.config, 'r') as f:
    myconfig = json.load(f)

for switch in myconfig['switches']:
    logger.error(f'Switch: {switch}')
    with Device(host=switch, user=myconfig['config']['username'], password=myconfig['config']['password']) as jdev:  # noqa E501
        res = jdev.cli('show chassis hardware', warning='False')
        members = re.findall(r'^FPC.*', res, re.MULTILINE)
        for member in members:
            print(member)
        print("-----------------------------------------------------------\n")
