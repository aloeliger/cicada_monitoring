# Utility class for holding data that will be reported to the CICADA mattermost
# Will build and hold the data

from .bot_functions import *
import datetime
import copy
import time
import random

class CICADA_bot_data():
    def __init__(self, config: dict, auth):
        self.config = config
        self.run_json = None
        self.cicada_trigger_list = None
        self.auth = auth

    # Trigger the data building request functions, and store the results
    # for the bot to later report on
    def build_data(self) ->  None:
        today = datetime.date.today()
        today_datetime = datetime.datetime(today.year, today.month, today.day)
        start_date = today - datetime.timedelta(days=self.config["nDays"])
        start_date_datetime = datetime.datetime(start_date.year, start_date.month, start_date.day)
        
        run_json = get_list_of_runs(
            self.auth,
            start_date_datetime,
            today_datetime
        )        

        run_json = filter_runs(run_json)
        cicada_triggers_per_run = []
        for index, run in enumerate(run_json['data']):
            
            run_json['data'][index] = get_cicada_rates_for_run(self.auth, run)
            cicada_triggers_per_run.append(list(run['CICADA_physics_trigger_rates'].keys()))
        self.run_json = run_json
        #Let's also compile a list of lists of cicada trigger bits
        #Then get the intersection of all them
        self.unique_cicada_triggers = list(
            set.union(*[set(x) for x in cicada_triggers_per_run])
        )

    # Convenience function for making a markdown table to report to mattermost
    def build_markdown_table(self) -> str:
        if self.run_json is None:
            raise RuntimeError("Data has not been built by this data class instance. Call build_data() first, before markdown of the information can be generated")

        # Top row of markdown
        trigger_list = copy.deepcopy(self.unique_cicada_triggers)
        trigger_list.sort()
        the_table = '|run'
        for cicada_trigger in trigger_list:
            the_table+=f'|{cicada_trigger} (Hz)'
        #Second row of markdown
        the_table+='|\n|:---:'
        for cicada_trigger in self.unique_cicada_triggers:
            the_table+='|:---:'
        the_table += '|\n'

        for run in self.run_json['data']:
            the_table += f'|{run["id"]}'
            for cicada_trigger in trigger_list:
                rate = 0.0
                try:
                    rate = run["CICADA_physics_trigger_rates"][cicada_trigger]
                except KeyError:
                    rate = 'N/A'
                the_table+=f'|{rate}'
            the_table += '|\n'
        return the_table
