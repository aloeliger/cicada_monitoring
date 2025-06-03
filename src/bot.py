# The bot structure that will report to mattermost

from .bot_data import *
from .bot_functions import *

from dotenv import load_dotenv
import os

import json

class cicada_bot():
    def __init__(self, config_path):
        load_dotenv()
        self.mattermost_api_url = os.environ['API_URL']

        with open(config_path) as the_file:
            self.config = json.load(the_file)

        self.data = None

    #Get the latest instance of OMS data
    def update_data(self):
        import tsgauth.oidcauth
        auth = tsgauth.oidcauth.DeviceAuth("cmsoms-prod-public",target_client_id="cmsoms-prod",use_auth_file=True)
        self.data = CICADA_bot_data(self.config, auth)
        self.data.build_data()

    def make_markdown_table_post(self, markdown_table):
        post_contents=f'CICADA Rates for collisions runs for the last {self.config["nDays"]} days\n'
        request_headers = {
            'Content-Type': 'application/json'
        }
        
        request_contents = {
            "attachments": [
                {
                    "text": post_contents
                },
                {
                    "fallback": "Table data",
                    "text": markdown_table
                }
            ]
        }
        
        result = requests.post(self.mattermost_api_url, data=json.dumps(request_contents), headers=request_headers)
        result.raise_for_status()
        
    #Overall holder function for all the various things that the bot
    #should do on an update
    def update(self):

        #First step, update our data
        self.update_data()

        #now, let's get our markdown table
        markdown_table = self.data.build_markdown_table()
        # and we'll post it to mattermost
        self.make_markdown_table_post(markdown_table)
