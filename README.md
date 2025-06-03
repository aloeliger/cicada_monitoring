### Setup

```
#No CMSSW required, just python and a virtual environment
git clone --recursive git@github.com:aloeliger/cicada_monitoring.git
cd cicada_monitoring
python3 -m pip venv cicada_monitoring_env
source cicada_monitoring_env/bin/activate #if using bash.
python3 -m pip install -r requirements.txt

#You will need a .env file containing the mattermost webhook api URL
#Contact the repo maintainer to get it
python3 cicada_monitoring.py
```

The bot itself will, by default, totally occupy the shell it is in, so it can be run in the background with `&`, however, I recommend
running it inside a tmux session where it can be left alone in it's own shell, because every so often it may provide a link that must
be followed to refresh OMS credentials that shouldn't get lost, otherwise the bot will need to be restarted.

To actually report to mattermost, you will need a `.env` file at topmost level of the repository. The structure of this file needs to be

```
API_URL=<the_mattermost_webhook_url>
```

To get this URL, please contact a repository maintainer.

### Structure

#### `cidada_monitoring.py`
Central handling script. Creates a bot instance, and sets up a schedule for it to run.

#### Src/
Contains code and functions not central to the handling script

##### `bot_functions.py`
Contains functions for requesting and receiving data from OMS

##### `bot_data.py`
Contains a class for holding JSONs received from OMS. Uses `bot_functions.py` to call OMS, and then contains code for processing the results

##### `bot.py`
Contains a class with task and update logic

#### Test/
Contains unit tests. Please unit test any code added!
