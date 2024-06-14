#!/usr/bin/env python3

# I started by creating my initial cert using certbot
# I installed and setup using TinyPilot's directions:
# https://tinypilotkvm.com/faq/own-tls-key/
# I later added this as a renew_hook.

import paramiko

LE_DIR = '/etc/letsencrypt/live'
HOSTNAME = 'my.hostname.goes.here'
USERNAME = 'pilot'
SSHKEY = '/path/to/tinypilot.id_ed25519'
CERT = f'{LE_DIR}/{HOSTNAME}/cert.pem'
PRIVKEY = f'{LE_DIR}/{HOSTNAME}/privkey.pem'
REMOTE_TEMP_CERT = '/tmp/temp-cert.pem'
REMOTE_TEMP_PRIVKEY = '/tmp/temp-privkey.pem'
REMOTE_CERT = '/etc/ssl/certs/tinypilot-nginx.crt'
REMOTE_PRIVKEY = '/etc/ssl/private/tinypilot-nginx.key'

# Setup SSH Session
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOSTNAME, username=USERNAME, key_filename=SSHKEY)

# Transfer new cert and key files
sftp_client = client.open_sftp()
sftp_client.put(CERT, REMOTE_TEMP_CERT)
sftp_client.put(PRIVKEY, REMOTE_TEMP_PRIVKEY)
sftp_client.close()

# Backup old cert and key files
_stdin, _stdout, _stderr = client.exec_command(f"sudo cp {REMOTE_CERT} {REMOTE_CERT}.backup")  # noqa: E501
print(_stdout.read().decode())
_stdin, _stdout, _stderr = client.exec_command(f"sudo cp {REMOTE_PRIVKEY} {REMOTE_PRIVKEY}.backup")  # noqa: E501
print(_stdout.read().decode())

# Copy new cert and key files into position, restart nginx
_stdin, _stdout, _stderr = client.exec_command(f"sudo cp {REMOTE_TEMP_CERT} {REMOTE_CERT}")  # noqa: E501
print(_stdout.read().decode())
_stdin, _stdout, _stderr = client.exec_command(f"sudo cp {REMOTE_TEMP_PRIVKEY} {REMOTE_PRIVKEY}")  # noqa: E501
print(_stdout.read().decode())
_stdin, _stdout, _stderr = client.exec_command("sudo service nginx restart")
print(_stdout.read().decode())

# Cleanup temp files
_stdin, _stdout, _stderr = client.exec_command(f"sudo rm {REMOTE_TEMP_CERT} {REMOTE_TEMP_PRIVKEY}")  # noqa: E501
print(_stdout.read().decode())

client.close()
