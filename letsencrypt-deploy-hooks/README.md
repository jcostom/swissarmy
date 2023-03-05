# How Do I Use These?

Deploy Hooks are super useful. These are scripts that execute upon successful renew operations. So, how do you add these to your `certbot` certs? Too easy.

Get `certbot` installed on your system using their directions. That's outside the scope of what I'm doing here. For me, I did it using the `snap` packages on Ubuntu 20.04 and 22.04 hosts. It was super easy.

Now mind you, I'm using these scripts for use cases where I'm using the `certbot certonly` type syntax, where I'm only generating certs, not using `certbot`'s installation capabilities. So, that's why these scripts make sense. I've got 5 different use cases here that I'm leveraging.

1. `edgeos-renew.py` - Installs the cert on a Ubiquiti EdgeRouter.
1. `hpm479-cert.sh` - Installs the cert on an HP Color LaserJet Pro M479 series printer
1. `plex-cert.sh` - Installs the cert in a Docker container for the Plex Media Server
1. `unbound-cert.sh` - Restarts the Unbound DNS service after the certs update
1. `unifi-cert.sh` - Installs the cert in a Docker container for the UniFi WLAN controller (the `jacobalberty/unifi` flavor).

I've dropped these scripts on my system in `/usr/local/sbin`, and made sure they're executable (ie, chmod 700, files are owned root:root).

In order to update your automatic renewal configuration to add the script just takes a couple of commands. First a dry-run, then you force the renewal. If you've got a lot to do, you might get rate-limited, so be careful. For me, here's what it looked like:

```bash
sudo certbot renew --cert-name printer.home.[redacted].net --deploy-hook /usr/local/sbin/printer-renew.sh --dry-run
sudo certbot renew --cert-name printer.home.[redacted].net --deploy-hook /usr/local/sbin/printer-renew.sh --force-renewal
```

## Another Option To Consider

There's another option you've got to consider, but I'm not using here. There's the `/etc/letsencrypt/renewal-hooks/deploy` directory. While scripts that you run using the method prescribed up above run on a per-domain basis, this method will execute for every certificate renewed.

That might be useful for something you've got in mind. Maybe you're looking to do something like perhaps automatically archive new certs every time one updates or something like that, or maybe something else I'm just not thinking of right now. Whatever it is, you can do it. The cert that just got issued will be identified via an environment variable - the `$RENEWED_LINEAGE` variable, will point to the appropriate directory in `/etc/letsencrypt/live`, allowing you to reference filenames like `/etc/letsencrypt/live/${RENEWED_LINEAGE}/cert.pem`, etc. in your script.
