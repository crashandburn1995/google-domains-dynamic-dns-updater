#!/usr/bin/env python3
# This file updates a Google DDNS record with the WAN IP of the system running the script.

import requests
import ipaddress
from itertools import groupby

# The URL to use to update the Google DDNS record.
update_google_ddns_url = (
    "https://{}:{}@domains.google.com/nic/update?hostname={}&myip={}"
)

# The maximum number of times to attempt to get the WAN IP.
wan_ip_retrieval_retry_attempts = 3

# Google DDNS credentials and hostname.
username = ""
password = ""
hostname = ""

# URLs which return the requestor's WAN IP.
urls_which_return_requestor_ip_address = [
    "https://icanhazip.com",
    "https://ifconfig.me",
    "https://api.ipify.org",
    "https://ipinfo.io/ip",
    "https://ipecho.net/plain",
]


# This function checks whether all of the items in the iterable match.
def all_equal(iterable) -> bool:
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


# This function makes a request to a web server and returns an ip address.
# It returns an IP address or an exception.
def get_ip_address_from_web_server(url: str) -> ipaddress.ip_address:
    request_result = requests.get(url)
    if not request_result.ok:
        raise ValueError("The request to get an IP address was not successful.")

    request_result = request_result.text.strip()
    if len(request_result) == 0:
        raise ValueError(
            "There is no data in the result returned from the request to get an IP address."
        )

    return ipaddress.ip_address(request_result)


# This function makes requests to multiple web servers which return an IP address.
# It returns a list of IP addresses or an exception.
def get_ip_addresses_from_multiple_web_servers(urls: list) -> list:
    returned_ip_addresses = []
    for url in urls:
        ip_address = get_ip_address_from_web_server(url)
        returned_ip_addresses.append(ip_address)

    return returned_ip_addresses


if __name__ == "__main__":
    if not username:
        raise ValueError("The Google DDNS username is empty.")

    if not password:
        raise ValueError("The Google DDNS password is empty.")

    if not hostname:
        raise ValueError("The Google DDNS hostname is empty.")

    # Attempt to get the WAN IP and retry if there is an error (up to the configured number of retry attempts).
    for attempt in range(wan_ip_retrieval_retry_attempts):
        # Get the WAN IP from multiple sources.
        try:
            ip_addresses = get_ip_addresses_from_multiple_web_servers(
                urls_which_return_requestor_ip_address
            )
        except:
            continue

        # If all of the IPs match, then exit the loop. Otherwise, try again.
        if all_equal(ip_addresses):
            break
    else:
        raise ValueError(
            "The maximum number of attempts to get the WAN IP was exceeded."
        )

    wan_ip = ip_addresses[0]

    # Send request to Google DDNS to update the DNS record with the WAN IP.
    update_google_ddns_request_result = requests.post(
        update_google_ddns_url.format(username, password, hostname, wan_ip)
    )

    # If an error occurs, raise an exception with the error information.
    if not update_google_ddns_request_result.ok:
        raise ValueError(
            "The following error occurred when updating the Google Dynamic DNS entry: {}".format(
                update_google_ddns_request_result.text
            )
        )

    success_message = "Google Dynamic DNS update request successful: {}".format(
        update_google_ddns_request_result.text
    )

    # Print the success message.
    print(
        success_message,
        flush=True,
    )
