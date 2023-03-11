"""A clean API Google Calendar client."""

import dataclasses
import datetime
from typing import List, Optional

import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import credentials as gcreds

# class GmailClient:
class GmailClient:
    """A wrapper around Gmail API to return clean objects for consumption.

    The API doc can be found here:
        https://developers.google.com/gmail/api/guides/
    """

    def __init__(self, access_token: str):
        self.client = googleapiclient.discovery.build(
            "gmail",
            "v1",
            credentials=gcreds.Credentials(token=access_token),
            static_discovery=False,
        )

    def threads(
        self,
    ):

        threads = self.client.users().threads().list(userId='me').execute().get('threads', [])
        for thread in threads:
            tdata = self.client.users().threads().get(userId='me', id=thread['id']).execute()
            nmsgs = len(tdata['messages'])

            # skip if <3 msgs in thread
            if nmsgs > 2:
                msg = tdata['messages'][0]['payload']
                subject = ''
                for header in msg['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                if subject:  # skip if no Subject line
                    print(F'- {subject}, {nmsgs}')
        return threads
