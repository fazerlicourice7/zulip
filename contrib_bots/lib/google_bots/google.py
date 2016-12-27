#!/usr/bin/env python
from __future__ import print_function
import datetime
import httplib2
import os

from oauth2client import client, tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# This file contains the information that google uses to figure out which application is requesting
# this client's data.
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Zulip'
HOME_DIR = os.path.expanduser('~')


def get_credentials(scopes):
    # type: () -> client.Credentials
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    credential_path = os.path.join(HOME_DIR,
                                   'google-credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(HOME_DIR, CLIENT_SECRET_FILE), scopes)
        flow.user_agent = APPLICATION_NAME
        if flags:
            # This attempts to open an authorization page in the default web browser, and asks the user
            # to grant the bot access to their data. If the user grants permission, the run_flow()
            # function returns new credentials.
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials
