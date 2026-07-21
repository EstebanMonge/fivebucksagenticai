#!/usr/bin/env python3

import argparse
import re
import sys
import time

import requests
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    ReadTimeout,
    SSLError,
    InvalidURL,
    TooManyRedirects,
    RequestException
)
import socket

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def exit_plugin(state, message):
    print(message)
    sys.exit(state)


parser = argparse.ArgumentParser()

parser.add_argument("-u", "--url", required=True,
                    help="Odoo base URL (example: http://host)")

parser.add_argument("-P", "--port", type=int,
                    help="Odoo port (example: 8069)")

parser.add_argument("-l", "--login", required=True,
                    help="Login/email")

parser.add_argument("-p", "--password", required=True,
                    help="Password")

parser.add_argument("-t", "--timeout", type=int, default=10,
                    help="Timeout")

args = parser.parse_args()

base_url = args.url.rstrip("/")

if args.port:
    # Remove an existing port if one is already present
    m = re.match(r'^(https?://[^/:]+)(?::\d+)?$', base_url)
    if m:
        base_url = f"{m.group(1)}:{args.port}"
    else:
        exit_plugin(UNKNOWN, "UNKNOWN - Invalid URL format")

login_url = f"{base_url}/web/login"

try:
    session = requests.Session()

    start = time.time()

    #
    # Step 1 - GET login page
    #
    response = session.get(login_url, timeout=args.timeout)

    if response.status_code != 200:
        exit_plugin(
            CRITICAL,
            f"CRITICAL - Login page returned HTTP {response.status_code}"
        )

    #
    # Step 2 - Extract csrf_token
    #
    match = re.search(
        r'name="csrf_token"\s+value="([^"]+)"',
        response.text
    )

    if not match:
        exit_plugin(
            CRITICAL,
            "CRITICAL - Unable to locate csrf_token"
        )

    csrf_token = match.group(1)

    #
    # Step 3 - POST credentials
    #
    payload = {
        "csrf_token": csrf_token,
        "login": args.login,
        "password": args.password,
        "redirect": "",
        "type": "password",
    }

    headers = {
        "Referer": login_url,
        "User-Agent": "Nagios Odoo Login Check"
    }

    response = session.post(
        login_url,
        data=payload,
        headers=headers,
        timeout=args.timeout,
        allow_redirects=True
    )

    elapsed = time.time() - start

    #
    # Step 4 - Verify login
    #

    #
    # Invalid credentials
    #
    if "Wrong login/password" in response.text:
        exit_plugin(
            CRITICAL,
            "CRITICAL - Invalid username or password"
        )

    #
    # Login page again => failed
    #
    if 'name="login"' in response.text and \
       'name="password"' in response.text:
        exit_plugin(
            CRITICAL,
            "CRITICAL - Login failed"
        )

    #
    # Successful session
    #
    if "/web/session/logout" in response.text \
            or "/web#" in response.url \
            or "session_info" in response.text \
            or "odoo.__session_info__" in response.text:

        print(f"OK - Login successful ({elapsed:.2f} sec)")
        sys.exit(OK)

    exit_plugin(
        CRITICAL,
        "CRITICAL - Login status unknown"
    )

except requests.exceptions.Timeout:
    exit_plugin(CRITICAL, "CRITICAL - Connection timeout")

except ConnectTimeout:
    exit_plugin(CRITICAL, "CRITICAL - Connection timed out")

except ReadTimeout:
    exit_plugin(CRITICAL, "CRITICAL - Server did not respond in time")
except SSLError as e:
    exit_plugin(CRITICAL, f"CRITICAL - SSL error: {e}")

except InvalidURL:
    exit_plugin(UNKNOWN, "UNKNOWN - Invalid URL")

except TooManyRedirects:
    exit_plugin(CRITICAL, "CRITICAL - Too many HTTP redirects")

except ConnectionError as e:
    msg = str(e)

    if "NameResolutionError" in msg or "Failed to resolve" in msg:
        exit_plugin(
            CRITICAL,
            f"CRITICAL - Unable to resolve hostname '{args.url}'"
        )

    if "Connection refused" in msg:
        exit_plugin(
            CRITICAL,
            "CRITICAL - Connection refused"
        )

    if "No route to host" in msg:
        exit_plugin(
            CRITICAL,
            "CRITICAL - No route to host"
        )

    exit_plugin(CRITICAL, f"CRITICAL - Connection error: {msg}")

except socket.gaierror:
    exit_plugin(
        CRITICAL,
        f"CRITICAL - Unable to resolve hostname '{args.url}'"
    )

except RequestException as e:
    exit_plugin(CRITICAL, f"CRITICAL - HTTP request failed: {e}")

except Exception as e:
    exit_plugin(UNKNOWN, f"UNKNOWN - {type(e).__name__}: {e}")
