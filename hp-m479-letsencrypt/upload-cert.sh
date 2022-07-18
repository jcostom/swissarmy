#!/usr/bin/env bash

# Certificate expects to find your cert in the usual location for certbot
# managed certs. Run this script out of cron, and your printer's cert will
# always be up to date, assuming certbot's configured to automatically
# renew your certs.
# 
# This works for me on my HP LJ MFP 479fdw. YMMV. On other models you may
# need to adjust the URL. You'll want to use Chrome's developer tools or
# even just good old view source to work out the details of what URL you
# need to post the info to...

HOSTDIR=/etc/letsencrypt/live/printer.domain.net
OUTFILE=/var/tmp/printer.p12
PASS=exportPassword
PRINTERAUTH=admin:adminPassword
URL="https://printer.domain.net/Security/DeviceCertificates/NewCertWithPassword/Upload?fixed_response=true"

# combine key and cert into PKCS12 package
openssl pkcs12 -export -out "${OUTFILE}" -inkey "${HOSTDIR}"/privkey.pem -in "${HOSTDIR}"/cert.pem -passout pass:"${PASS}"

# upload package to printer
curl -u "${PRINTERAUTH}" --insecure "${URL}" -F certificate=@"${OUTFILE}" -F password="${PASS}"

# remove temp file
rm "${OUTFILE}"