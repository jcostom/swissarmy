# purge-unifi-db.js

UniFi running slow? Out of disk space? Just want to purge old logs from the database?

Before you start, please read through the code and try to understand what's going on.

There are a couple of variables at the very top that you need to pay attention to. First is the number of days worth of data you want to keep in the database after the purge is complete. The default is set at 7. Change it to whatever you like, or leave it at 7. You do you.

The other variable is set to either "true" or "false". It's the `dryrun` variable. It's what determines if you're just kicking the tires, or if you're really and truly purging the data from the database.

Ready to go? Ok...

Contrary to what you'd expect, with the Unifi service running, run the following:

`mongo --port 27117 < purge-unifi-db.js`

It will churn for a moment or two, or 30, depending on the size of your database. Then you'll be able to see the results.

Please, I beg of you. Have good backups ***BEFORE*** you start doing something like this. You never know what could go wrong. If you blow your stuff up, I'm sorry, but it's really not my fault, and I did warn you to backup before you start messing around in the bowels of your WLAN controller.
