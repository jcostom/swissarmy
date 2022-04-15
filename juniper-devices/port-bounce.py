#!/usr/bin/env python3

"""
You ever need to bounce a port on a system, but don't
want to, or just plain can't walk up to the system
and pull a cable out? Don't feel like doing the
disable/commit/enable/commit dance manually?
This does the work for you.

Yes, you could also drop to a root shell and
use ifconfig, but JTAC doesn't exactly look
fondly on that. So don't do that. Plus, "unexpected"
consequences could occur from that, and who likes those?
So do this instead, ok?

The only non-default module here is PyEZ. Installation
directions for the module found here:
https://github.com/Juniper/py-junos-eznc
"""

import argparse
import os
import logging
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# Setup logger
logger = logging.getLogger()
ch = logging.StreamHandler()
logger.setLevel(logging.ERROR)
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

parser = argparse.ArgumentParser(
    description='Juniper Device Port Bounce Utility'
)

parser.add_argument('--sys', action="store")
parser.add_argument('--port', action="store")
parser.add_argument('--user', action="store",
                    default=os.getenv('USER'),
                    help="Will default to your current username.")
parser.add_argument('--password', action="store",
                    help="Omit this option if you're using ssh keys to authenticate")  # noqa: E501
args = parser.parse_args()


def main():
    disableCommand = " ".join(
        ["set interfaces", args.port, "disable"]
    )
    disableComment = " ".join(
        ["shut port", args.port]
    )
    rollbackComment = " ".join(
        ["rollback shut of port", args.port]
    )

    dev = Device(host=args.sys, user=args.user, password=args.password)
    logger.error(f"Connecting to: {args.sys}")
    dev.open()
    dev.bind(cu=Config)
    logger.error(f"Locking the configuration on: {args.sys}")
    dev.cu.lock()
    logger.error(f"Now shutting port: {args.port}")
    dev.cu.load(disableCommand, format='set')
    dev.cu.commit(comment=disableComment, timeout=180)
    logger.error(f"Now executing rollback on: {args.sys}")
    dev.cu.rollback(rb_id=1)
    dev.cu.commit(comment=rollbackComment, timeout=180)
    logger.error(f"Unlocking the configuration on: {args.sys}")
    dev.cu.unlock()
    dev.close()
    logger.error("Done!")


if __name__ == "__main__":
    main()
