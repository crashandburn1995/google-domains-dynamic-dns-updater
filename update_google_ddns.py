#!/usr/bin/env python3
# This file updates a Google DDNS record with the WAN IP of the system running the script.

import requests
import ipaddress
from itertools import groupby

# The URL to use to update the Google DDNS record.
update_google_ddns_url = (
    "https://{}:{}@domains.google.com/nic/update?hostname={}&myip={}"
)

# The number of times to attempt to get the WAN IP.
ip_retrieval_attempts = 3

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
        raise ValueError("Request was not successful.")

    request_result = request_result.text.strip()
    if len(request_result) == 0:
        raise ValueError("There is no data in the request result.")

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
    # Attempt to get the WAN IP up to 3 times before exiting.
    for attempt in range(ip_retrieval_attempts):
        # Get the WAN IP from multiple sources.
        ip_addresses = get_ip_addresses_from_multiple_web_servers(
            urls_which_return_requestor_ip_address
        )

        # If the WAN IP matches, then exit the loop. Otherwise, try again.
        if all_equal(ip_addresses):
            break
    else:
        # If after 3 times the IP address doesn't match, exit the program.
        raise ValueError("IP addresses not equal.")

    current_ip = ip_addresses[0]

    # Send request to Google DDNS to update the IP.
    update_ddns_request = requests.post(
        update_google_ddns_url.format(username, password, hostname, current_ip)
    )

    # If an error occurs, print it to the console.
    if not update_ddns_request.ok:
        raise ValueError(
            "An error occurred when updating the domain: {}".format(
                update_ddns_request.text
            )
        )

    # Otherwise, print the success message.
    print(
        "DDNS update request successful: {}".format(update_ddns_request.text),
        flush=True,
    )
