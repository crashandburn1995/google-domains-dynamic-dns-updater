# Update Google Dynamic DNS Script
This script updates a Google Dynamic DNS record for a domain from Google Domains.

I created this script so that my Unifi Dream Router would automatically update my Google Domain with my WAN IP. This would then enable me to use a WireGuard VPN behind NAT. Though, this script should work on any system that can run Python 3.

I ran this on the following device and firmware:
```
Model:       UniFi Dream Router
Version:     3.0.17.9190
```

## Instructions for Unifi Devices
1. Replace the `username`, `password` and `hostname` values in `update_google_ddns.py` with:
    - Username -> The username in the `view credentials` window in Google Domains Dynamic DNS.
    - Password -> The password in the `view credentials` window in Google Domains Dynamic DNS.
    - Hostname -> The host name for the Dynamic DNS entry (e.g. `remoteaccess.mysite.com`).
2. Enable SSH on your Unifi device, login as root and upload this repository to `/root`. Once complete you will have a directory at `/root/google-domains-dynamic-dns-updater`. It will contain `update_google_ddns.sh` and `update_google_ddns.py`.
3. Setup a cron job to make the bash script run periodically. The following command can be used on the Unifi device to do this:
    ```
    (crontab -u root -l; echo "* */5 * * * /root/google-domains-dynamic-dns-updater/update_google_ddns.sh" ) | crontab -u root -
    ```
    The cron job timing can be adjusted as desired.
4. The cron job should now be updating your Dynamic DNS entry periodically. The script outputs a log to `/var/log/messages`, you can see the log with `tail -f /var/log/messages`.