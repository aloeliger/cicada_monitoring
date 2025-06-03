import pytest
from unittest.mock import patch, MagicMock

from cicada_monitoring.src.bot_data import *
from cicada_monitoring.test.test_bot_functions import run_result_json, algorithm_result_json
import json
import re

@pytest.fixture
def bot_config():
    with open("config/cicada_bot_config.json") as the_file:
        config_json = json.load(the_file)
    return config_json

def test_CICADA_bot_data(bot_config):
    auth = MagicMock()
    bot_data = CICADA_bot_data(bot_config, auth)

@pytest.fixture
def standard_bot_data(bot_config):
    auth = MagicMock()
    bot_data = CICADA_bot_data(bot_config, auth)
    return bot_data

#Not a good test. It basically rigs the test to succeed.
@patch('cicada_monitoring.src.bot_data.get_list_of_runs')
@patch("cicada_monitoring.src.bot_data.requests.get")
def test_build_data(mock_get, mock_get_list_of_runs, standard_bot_data, run_result_json, algorithm_result_json):
   mock_get_list_of_runs.return_value = run_result_json

   mock_response = MagicMock()
   mock_response.json.return_value = algorithm_result_json
   mock_get.return_value = mock_response
   
   standard_bot_data.build_data()
   
   assert(standard_bot_data.run_json is not None)
   assert(isinstance(standard_bot_data.run_json, dict))
    
   assert("L1_CICADA_Medium" in standard_bot_data.unique_cicada_triggers)

@patch('cicada_monitoring.src.bot_data.get_list_of_runs')
@patch("cicada_monitoring.src.bot_data.requests.get")
def test_build_markdown_table(mock_get, mock_get_list_of_runs, standard_bot_data, run_result_json, algorithm_result_json):
    mock_get_list_of_runs.return_value = run_result_json
    
    mock_response = MagicMock()
    mock_response.json.return_value = algorithm_result_json
    mock_get.return_value = mock_response
    
    standard_bot_data.build_data()
    
    markdown_table = standard_bot_data.build_markdown_table()

    assert(re.search('Hz', markdown_table) is not None)
    assert(re.search('L1_CICADA', markdown_table) is not None)

