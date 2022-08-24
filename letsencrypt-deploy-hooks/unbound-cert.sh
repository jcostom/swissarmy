#!/usr/bin/env bash

# My Unbound configuration directly references the cert.pem 
# and privkey.pem files that live in the /etc/letsencrypt/... 
# hierarchy. So, all that's needed is to restart the service.

systemctl restart unbound.service
