#!/usr/bin/env bash

# This works on my HP Color LaserJet Pro MFP M479fdw.
# Maybe it works for your HP that's a different model, maybe not.
# Maybe it makes your toaster catch on fire. If that happens, it's
# not my fault. I warned you.
#
# To customize for other HP printers, get into the Dev Tools in your
# browser, do some posts to the page with the dev tools up and logging
# your session. It shouldn't be too hard to work out what you need to 
# do to make it happen. I did it in a couple of hours, I'm sure you can
# too.

# this is the directory that certbot keeps your certs in
HOSTDIR=/etc/letsencrypt/live/fqdn.of.your.printer.net

# this is a temp PKCS12 package pre-installation
OUTFILE=/var/tmp/printer.pfx

# what your printer expects to use as a password to decrypt the cert
PASS=my-amazing-cert-password

# auth info and the URL to the printer page to post the certificate to
PRINTERAUTH=admin:printer-webui-password
URL="https://fqdn.of.your.printer.net/Security/DeviceCertificates/NewCertWithPassword/Upload?fixed_response=true"

# combine key and cert into PKCS12 package
openssl pkcs12 -export -out "${OUTFILE}" -inkey "${HOSTDIR}"/privkey.pem -in "${HOSTDIR}"/cert.pem -passout pass:"${PASS}"

# upload package to printer
curl -u "${PRINTERAUTH}" --insecure "${URL}" -F certificate=@"${OUTFILE}" -F password="${PASS}"

# remove temp file
rm "${OUTFILE}"
