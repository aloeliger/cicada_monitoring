import pytest
from unittest.mock import patch, MagicMock

from cicada_monitoring.src.bot import *

from cicada_monitoring.test.test_bot_data import standard_bot_data

@pytest.fixture
def config_path():
    return "config/cicada_bot_config.json"

def test_create_cicada_bot(config_path):
    bot = cicada_bot(config_path)
    assert(bot is not None)

#TODO: the update_data is hard to unit test due to the import
#TODO: find a way to test the various calls and posts
