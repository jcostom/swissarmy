#!/usr/bin/env python3

"""
This tool is a blunt instrument - HANDLE WITH CARE.
It disables PoE on all ports, commits the configuration,
then executes a rollback 1 and commits again.

You would only use this tool if you wanted to completely
disable PoE then rollback that change.

The only non-default module here is PyEZ. Installation
directions for the module found here:
https://github.com/Juniper/py-junos-eznc
"""

import argparse
import logging
import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# Setup logger
LOG_LEVEL = 'ERROR'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(asctime)s] %(message)s')
logger = logging.getLogger()

parser = argparse.ArgumentParser(
    description='Juniper Switch PoE Bounce Utility'
)

parser.add_argument('--switch', action="store")
parser.add_argument('--user', action="store",
                    default=os.getenv('USER'),
                    help="Will default to your current username.")
parser.add_argument('--password', action="store",
                    help="Omit this option if you're using ssh keys to authenticate")  # noqa: E501
args = parser.parse_args()


def main():
    disable_command = "set poe interface all disable"
    disable_comment = "drop the PoE sledgehammer on all ports"
    rollback_comment = "rollback - restoring PoE"

    dev = Device(host=args.switch, user=args.user, password=args.password)
    logger.error(f"Connecting to: {args.switch}")
    dev.open()
    dev.bind(cu=Config)
    logger.error(f"Locking the configuration on: {args.switch}")
    dev.cu.lock()
    logger.error("Now shutting down PoE on all ports.")
    dev.cu.load(disable_command, format='set')
    dev.cu.commit(comment=disable_comment, timeout=180)
    logger.error(f"Now executing rollback on: {args.switch}")
    dev.cu.rollback(rb_id=1)
    dev.cu.commit(comment=rollback_comment, timeout=180)
    logger.error(f"Unlocking the configuration on: {args.switch}")
    dev.cu.unlock()
    dev.close()
    logger.error("Done!")


if __name__ == "__main__":
    main()
