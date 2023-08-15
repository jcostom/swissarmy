#!/usr/bin/env python3

import logging
import os
import requests
import tempfile
import urllib3
import OpenSSL

# Ordinarily set this to 0. Change to 1 if you've got trouble.
DEBUG = 0

# Cert Info
LE_DIR = '/etc/letsencrypt/live'
PCKS12_PASSWORD = 'my-amazing-cert-password'

# Printer Info
DEVICE = 'myprinter.somesite.org'  # Or use IP address
AUTH_USER = 'my-printer-username'
AUTH_PASSWORD = 'my-printer-password'
URL = f'https://{DEVICE}/Security/DeviceCertificates/NewCertWithPassword/Upload?fixed_response=true'  # noqa E501

# Setup logger
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
logging.basicConfig(level=LOG_LEVEL,
                    format='[%(levelname)s] %(asctime)s %(message)s',
                    datefmt='[%d %b %Y %H:%M:%S %Z]')
logger = logging.getLogger()

# Let's prevent warnings for letsencrypt certs...
# Certbot will show these as errors
# The actual push succeeded without this because of the
# verify=False knob being set, but let's keep it nice
# looking.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # noqa E501

# Read cert and private key
cert_pem = f'{LE_DIR}/{DEVICE}/cert.pem'
privkey_pem = f'{LE_DIR}/{DEVICE}/privkey.pem'

with open(cert_pem, 'rb') as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())  # noqa E501

with open(privkey_pem, 'rb') as f:
    privkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())  # noqa E501

# Create temporary PKCS12 package to push to printer
pkcs = OpenSSL.crypto.PKCS12()
pkcs.set_privatekey(privkey)
pkcs.set_certificate(cert)
handle, output = tempfile.mkstemp(suffix='.pfx', dir='/var/tmp')
with open(output, 'wb') as f:
    f.write(pkcs.export(passphrase=PCKS12_PASSWORD.encode()))

# Prepare the request
files = {
    'certificate': open(output, 'rb'),
    'password': (None, PCKS12_PASSWORD)
}

# Push Certificate to Printer
response = requests.post(URL, files=files, verify=False, auth=(AUTH_USER, AUTH_PASSWORD))  # noqa E501
logger.info(f"Certificate Request Complete, Status code was {response}")

# Cleanup temp files
os.unlink(output)
