#!/usr/bin/env bash

# this is the directory that certbot keeps your certs in
HOSTDIR=/etc/letsencrypt/live/fqdn.of.your.unifi.server.net

# the directory the cert gets installed into
DESTDIR=/var/docks/unifi/cert

# the uid and gid you run your plex container under
UID=myuser
GID=mygroup

# the name of your plex container
CONTAINER=unifi

rm "${DESTDIR}"/cert.pem.md5
for file in cert.pem privkey.pem chain.pem; do
  cp "${DESTDIR}/${file}" "${DESTDIR}/${file}".backup
  cp "${HOSTDIR}/${file}" "${DESTDIR}"
  chown "${UID}:${GID}" "${DESTDIR}/${file}"
done

docker restart "${CONTAINER}"
