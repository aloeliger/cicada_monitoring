import pytest
from unittest.mock import patch, MagicMock

import datetime
from cicada_monitoring.src.bot_functions import *
import json

@pytest.fixture
def run_result_json():
    with open("test/test_oms_runs.json") as the_file:
        result_json = json.load(the_file)
    return result_json

@pytest.fixture
def algorithm_result_json():
    with open("test/test_l1algorithm_self.json") as the_file:
        result_json = json.load(the_file)
    return result_json

@patch("cicada_monitoring.src.bot_functions.requests.get")
def test_get_list_of_runs(mock_get, run_result_json):
    mock_response = MagicMock()
    mock_response.json.return_value = run_result_json
    mock_get.return_value = mock_response
    mock_auth = MagicMock()
    
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    today_date = datetime.date.today()

    yesterday_start_time = datetime.datetime(yesterday_date.year, yesterday_date.month, yesterday_date.day)
    today_start_time = datetime.datetime(today_date.year, today_date.month, today_date.day)

    run_json = get_list_of_runs(mock_auth, yesterday_start_time, today_start_time)

    assert(isinstance(run_json, dict))

@patch("cicada_monitoring.src.bot_functions.requests.get")
def test_get_cicada_rates_for_run(mock_get, run_result_json, algorithm_result_json):
    mock_response = MagicMock()
    mock_response.json.return_value = algorithm_result_json
    mock_get.return_value = mock_response
    mock_auth = MagicMock()

    single_run_result_json = run_result_json['data'][0]
    run_json =  get_cicada_rates_for_run(mock_auth, single_run_result_json)

    assert(
        isinstance(run_json, dict)
    )
    assert(
        'L1_CICADA_Medium' in run_json['CICADA_trigger_rates']
    )

def test_run_json_filter_false(run_result_json):
    single_run_result_json = run_result_json['data'][0]
    filter_result = run_json_filter(single_run_result_json)
    assert(filter_result == False)

def test_run_json_filter_true(run_result_json):
    single_run_result_json = run_result_json['data'][1]
    filter_result = run_json_filter(single_run_result_json)
    assert(filter_result == True)

def test_filter_runs(run_result_json):
    final_run_result_json = filter_runs(run_result_json)
    assert(
        final_run_result_json['data'][0]['id'] == '392672'
    )
    assert(
        final_run_result_json['data'][0]['attributes']["l1_hlt_mode_stripped"] == "collisions2025/v40"
    )
