# DeFiChain Donation Bot

The task of this bot is to inform about incoming funds on a defined DFI address as tweet.


# Setup

* create own config.json with `cp config_example.json config.json` and add own values

* create an own twitter app: https://developer.twitter.com/en and add the app credentials to your config.json (consumer_key and consumer_secret)

* Run the `setup.py` and follow the instructions.

	- script will output the auth url for twitter
	- login to twitter and give auth access
	- enter the `PIN` in the setup process
	- copy/paste the `access_token` and `access_token_secret` to the `config.json`

* To monitor your DFI address, enter your DFI address in the `config.json` (attribute: `address`)

* In the config, you can edit the text of the tweet (attribute: `tweet_settings-base_text`)

* to test the script, you can disable the `send_tweet` flag and run the script (`python3 bot.py`)

* to run the bot periodically, you should add a cronjob to trigger it (e.g. hourly):
`0 * * * * python3 bot.py > bot_activity.log`