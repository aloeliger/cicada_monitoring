import schedule
import src.bot as bot

import argparse
import time

def main(args):
    cicada_bot = bot.cicada_bot(args.config_path)

    update_trigger = lambda : cicada_bot.update()

    #Every day at 18:00 Central (00:00 UTC) check the previous day's runs
    schedule.every().day.at("18:00").do(update_trigger)

    while True:
        schedule.run_pending()
        time.sleep(60*10) #We don't need to be that accurate, and we can save a few CPU cycles by just checking every 10 minutes or so if we need to do something.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automated bot to monitor CICADA rates and post it to mattermost')

    parser.add_argument(
        '--config_path',
        default='config/cicada_bot_config.json',
        help='Path to configuration json that helps configure the bot. Does not contain the webhook URL, which must be provided in a .env file',
        nargs='?',
    )

    args = parser.parse_args()

    main(args)
