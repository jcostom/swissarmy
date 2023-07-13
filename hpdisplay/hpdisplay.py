#!/usr/bin/env python3

# Python port of the old April Fools Day perl script to change the
# HP Printer Status Message via a PJL job. My current HPLJ doesn't
# support this amazing feature, so I can't test this right now.
# Please let me know if this doesn't work correctly. As near
# as I can tell, it should.

import argparse
import logging
import socket

# Setup logger
LOG_LEVEL = 'INFO'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(asctime)s] %(message)s')
logger = logging.getLogger()

parser = argparse.ArgumentParser(
    description='HP JetDirect Status Message Change Utility'
)
parser.add_argument("-i", "--ip", action="store", required=True,
                    help="IP of your printer.")
parser.add_argument("-m", "--message", action="store", required=True,
                    help="Text to change status message to.")
args = parser.parse_args()

ESC = '\x1b'
command = f'''{ESC}%-12345X@PJL JOB
@PJL RDYMSG DISPLAY="{args.message}"
@PJL EOJ
{ESC}%-12345X
'''


def main() -> None:
    logger.info(f'Changing status message on printer {args.ip} to "{args.message}"!')  # noqa E501
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.ip, 9100))
        s.sendall(command.encode('utf-8'))


if __name__ == "__main__":
    main()
