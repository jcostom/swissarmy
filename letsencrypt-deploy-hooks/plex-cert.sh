#!/usr/bin/env bash

# this is the directory that certbot keeps your certs in
HOSTDIR=/etc/letsencrypt/live/fqdn.of.your.plex.server.net

# this is a temp PKCS12 package pre-installation
EXPORT=/var/tmp/server.pfx

# where the cert will be installed to
PLEXDIR=/var/docks/plexconfig/certs

# what your plex server expects to use as a password to decrypt the cert
PASS=my-cert-password

# the uid and gid you run your plex container under
UID=myuser
GID=mygroup

# the name of your plex container
CONTAINER=plex


# combine key and cert into PKCS12 package
openssl pkcs12 -export -out "${EXPORT}" -inkey "${HOSTDIR}"/privkey.pem -in "${HOSTDIR}"/cert.pem -passout pass:"${PASS}"

# delete backup cert if exists
if [ -f "${PLEXDIR}"/server.pfx.backup ] ; then
    rm -f "${PLEXDIR}"/server.pfx.backup
fi

# create new backup
cp "${PLEXDIR}"/server.pfx "${PLEXDIR}"/server.pfx.backup

# copy new cert into place
cp "${EXPORT}" "${PLEXDIR}"/server.pfx
chown "${UID}:${GID}" "${PLEXDIR}"/server.pfx
rm -f "${EXPORT}"

# restart Plex
docker restart "${CONTAINER}"
