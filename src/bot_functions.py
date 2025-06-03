# Functions for making requests and compiling data for the bot

#Example successful filtering for runs based on date
#https://cmsoms.cern.ch/agg/api/v1/runs?filter[start_time][GE]=2025-05-29T00:00:00&filter[start_time][LE]=2025-05-30T00:00:00

import requests
import datetime
import re

# Given a start and end time (likely start of yesterday to start of today)
# Figure out which runs occurred
# We will then hand off this json, to another series of requests
def get_list_of_runs(auth, start_time: datetime.datetime, end_time:  datetime.datetime) -> dict:
    all_runs = []
    request_url = f'https://cmsoms.cern.ch/agg/api/v1/runs?filter[start_time][GE]={start_time.isoformat()}&filter[start_time][LE]={end_time.isoformat()}'
    run_json = requests.get(request_url, **auth.authparams(), verify=False).json()
    return run_json

# Once we have a series of run jsons, let's filter it down to runs we
# want to look at, largely collisions runs
def run_json_filter(run_json):
    hlt_mode = run_json['attributes']['l1_hlt_mode_stripped']
    if hlt_mode is None:
        return False
    if re.search(r'collision', run_json['attributes']['l1_hlt_mode_stripped']) is not None:
        return True
    return False

# Use the above filter
def filter_runs(all_run_json):
    data = all_run_json['data']
    data = list(filter(run_json_filter, data))
    all_run_json['data'] = data
    return all_run_json

#For each run, compile the rates for all CICADA seeds in that run
def get_cicada_rates_for_run(auth, run_json) -> dict:
    relationship_links = run_json['relationships']
    l1algorithms_link = relationship_links['l1algorithmtriggers']['links']
    final_lumi_number = int(run_json['attributes']['last_lumisection_number'])
    search_lumi = final_lumi_number//2
    #TODO: I am just guessing that we get more standard rates in the middle of the run.
    #We may want a better way to pick a lumi section
    algorithm_json = requests.get(l1algorithms_link['self']+'?page[limit]=1000'+f'&filter[lumisection_number][GE]={search_lumi}', **auth.authparams(), verify=False).json()

    rate_dict = {}
    physics_rate_dict = {}
    for trigger_algorithm in algorithm_json['data']:
        trigger_name = trigger_algorithm['attributes']['name']
        if not re.search(r'CICADA', trigger_name):
            continue
        rate_dict[trigger_name] = trigger_algorithm['attributes']['post_dt_rate']
        physics_rate_dict[trigger_name] = trigger_algorithm['attributes']['post_dt_physics_rate']

    run_json['CICADA_trigger_rates'] = rate_dict
    run_json['CICADA_physics_trigger_rates'] = physics_rate_dict
    
    return run_json
