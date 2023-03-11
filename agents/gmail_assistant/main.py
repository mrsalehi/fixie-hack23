"""Google Calendar agent example!

It can:
* Check your calendar for events.
* Find empty spots in your calendar.
* Schedule new meetings in your calendar.
"""


import datetime
import json
import sys

import fixieai
import gmail_client
import utils

try:
    oauth_params = fixieai.OAuthParams.from_client_secrets_file(
        "gcp-oauth-secrets.json",
        ["https://www.googleapis.com/auth/gmail.readonly"],
    )
except FileNotFoundError:
    print(
        "gcp-oauth-secrets.json was not found! You'll need to generate your own oauth "
        "to deploy this agent. For more info, follow the 4-step instructions here: "
        "https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow#creatingcred"
    )
    sys.exit(4)


BASE_PROMPT = """I am intelligent gmail assistant agent that can check your emails \
and generate responses to those emails. \
events by their title and time, unless the user asks for attendees or location."""


"""def getFewShots():
    import os
    folder_path = "C:/fixie/fixie-hack23/agents/trainingdata" # replace with the path to your folder containing text files
    files = os.listdir(folder_path)

    RecievedEmailsdata = {}
    SentEmailsdata = {}

    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r") as f:
                content = f.read()
                key = os.path.splitext(file)[0] # get the filename without the extension
                if "Recieved" in key:
                    RecievedEmailsdata[key] = content
                elif "Sent" in key:
                    SentEmailsdata[key] = content

    fewShots = ""

    for key, value in RecievedEmailsdata:
        responseKey = key.replace(".txt", "")

        responseKey =  responseKey+"response.txt"

        fewShots.add("Q: Answer the email " + value +  "[FUNCS]" + "A: " +
            SentEmailsdata)

    return fewShots     """

FEW_SHOTS = """
Q: What emails are in my inbox?
Thought: I need to get all emails from the inbox.
Func[list_emails] says: https://accounts.google.com/o/oauth2/auth?foo=bar
Thought: I need to pass the auth url to the user.
A: I don't have access to your inbox. Please authorize: https://accounts.google.com/o/oauth2/auth?foo=bar

Q: What emails are in my inbox?
Thought: I need to get all emails from the inbox.
Func[list_emails] says: {a long list of emails}
Thought: I need to summarize the emails.
A: Here are all your emails: {a long list of emails}

Q: Answer the emails I have got today
Thought: I need to get to the emails from gmail and then write draft responses
Func[dummyemails] says: [{"subject": "Urgent Cash Flow Situation",
"time": "13:10 11/03/2023",
"sender": "urgentinvestor@gmail.com",
"body":"Dear Matt,I regret to inform you that we are experiencing a significant cash flow problem, and we may not be able to meet our payroll obligations this week."

Func[respond_emails] says : [{"subject": "Urgent Cash Flow Situation",
"time": "13:10 11/03/2023",
"sender": "urgentinvestor@gmail.com",
"body":"Dear Investor"}]
A: Here is your draft {"subject": "Urgent Cash Flow Situation",
"body": "your response"}
"""

agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS, oauth_params=oauth_params)

def answeremail(query: fixieai.Message):
    print("this got called")


@agent.register_func
def workhours():
    """Returns valid working hours. Currently simple."""
    return "09:00 AM to 05:00 PM"


@agent.register_func
def list_emails(oauth_handler: fixieai.OAuthHandler, user_storage) -> str:
    """Returns all events in user's mailbox.
    """
    # del user_storage["_oauth_token"]
    user_token = oauth_handler.user_token()
    if user_token is None:
        url =  oauth_handler.get_authorization_url()
        # import pdb; pdb.set_trace()
        return url

    client = gmail_client.GmailClient(user_token)
    threads = client.threads()
    if threads:
        return "\n".join(f"{thread}" for thread in threads)
    else:
        return "You don't have any emails."
