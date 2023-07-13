#!/usr/bin/env python3

import logging
import tempfile
import os
from paramiko import AuthenticationException, SSHClient, AutoAddPolicy, SSHException  # noqa: E501
from scp import SCPClient

# set to keyfile or password
SSH_AUTH_METHOD = 'password'

# you'll always need these.
# Yes, even if you're authenticating via an ssh keypair, you still need the
# password. Why? The restart command needs to run via sudo.
DEVICE = 'my-router-hostname'
AUTH_USER = 'my-username'
AUTH_PASSWORD = 'my-password'

# If you set SSH_AUTH_METHOD to keyfile, you'll need these too.
# It's the path to the public key you're using, and its passphrase, if any.
AUTH_KEYFILE = ''
AUTH_PASSPHRASE = ''

# file names/locations
KNOWN_HOSTS = '/var/tmp/letsedgeos'
CERT_DIR = '/config/auth'
CERT_FILE = f'{CERT_DIR}/lets.pem'
LE_DIR = '/etc/letsencrypt/live'

# commands script executes over the SSH channel
BACKUP_COMMAND = f'cp {CERT_FILE} {CERT_FILE}.backup'
RESTART_COMMAND = 'systemctl restart lighttpd'

# Something wrong? Set to 1 and check out what's up.
DEBUG = 0

# Setup logger
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(levelname)s] %(asctime)s %(message)s',
                    datefmt='[%d %b %Y %H:%M:%S %Z]')
logger = logging.getLogger()


def main() -> None:
    # construct the cert file
    le_cert_file = f'{LE_DIR}/{DEVICE}/fullchain.pem'
    le_key_file = f'{LE_DIR}/{DEVICE}/privkey.pem'
    with open(le_cert_file, "r") as f:
        le_cert = f.read()

    with open(le_key_file, "r") as f:
        le_key = f.read()

    lets = le_cert + le_key
    handle, output = tempfile.mkstemp(suffix='.pem', dir='/var/tmp')
    with os.fdopen(handle, "w+") as f:
        f.write(lets)

    # setup ssh/scp connection
    if not os.path.exists(KNOWN_HOSTS):
        open(KNOWN_HOSTS, "w+").close()
        logger.info(f"{KNOWN_HOSTS} did not exist, creating empty file.")

    try:
        sshclient = SSHClient()
        sshclient.load_system_host_keys()
        sshclient.load_host_keys(KNOWN_HOSTS)
        sshclient.set_missing_host_key_policy(AutoAddPolicy())
        if SSH_AUTH_METHOD == 'password':
            sshclient.connect(DEVICE, username=AUTH_USER, password=AUTH_PASSWORD)  # noqa: E501
        else:
            sshclient.connect(DEVICE, username=AUTH_USER, key_filename=AUTH_KEYFILE, passphrase=AUTH_PASSPHRASE)  # noqa: E501

        # Backup existing cert file
        stdin, stdout, stderr = sshclient.exec_command(BACKUP_COMMAND)
        logger.info(f'STDOUT:{stdout.read().decode("utf8")}')
        logger.info(f'STDERR:{stderr.read().decode("utf8")}')
        logger.info(f'Return code: {stdout.channel.recv_exit_status()}')

        # transfer temp cert file
        scp = SCPClient(sshclient.get_transport())
        scp.put(output, remote_path='/var/tmp')

        # copy tempfile into position
        stdin, stdout, stderr = sshclient.exec_command(f'cp {output} {CERT_FILE}')  # noqa: E501
        logger.info(f'STDOUT:{stdout.read().decode("utf8")}')
        logger.info(f'STDERR:{stderr.read().decode("utf8")}')
        logger.info(f'Return code: {stdout.channel.recv_exit_status()}')

        # set file permissions
        stdin, stdout, stderr = sshclient.exec_command(f'chmod 400 {CERT_FILE}')  # noqa: E501
        logger.info(f'STDOUT:{stdout.read().decode("utf8")}')
        logger.info(f'STDERR:{stderr.read().decode("utf8")}')
        logger.info(f'Return code: {stdout.channel.recv_exit_status()}')

        # delete tempfile
        stdin, stdout, stderr = sshclient.exec_command(f'rm {output}')
        logger.info(f'STDOUT:{stdout.read().decode("utf8")}')
        logger.info(f'STDERR:{stderr.read().decode("utf8")}')
        logger.info(f'Return code: {stdout.channel.recv_exit_status()}')

        # restart lighttpd
        stdin, stdout, stderr = sshclient.exec_command(f"sudo -S -p '' {RESTART_COMMAND}")  # noqa: E501
        stdin.write(AUTH_PASSWORD + "\n")
        stdin.flush()
        logger.info(f'STDOUT:{stdout.read().decode("utf8")}')
        logger.info(f'STDERR:{stderr.read().decode("utf8")}')
        logger.info(f'Return code: {stdout.channel.recv_exit_status()}')

        # close streams
        stdin.close()
        stdout.close()
        stderr.close()
    except AuthenticationException:
        logger.debug("Authentication failed, check credentials.")
    except SSHException as sshException:
        logger.debug(f"Unable to establish SSH connection: {sshException}")
    finally:
        sshclient.close()

    # cleanup files
    os.unlink(output)
    os.unlink(KNOWN_HOSTS)


if __name__ == "__main__":
    main()
