import json
import time
import tweepy

def load_data():
    try:
        with open('config.json', 'r') as fp:
            data = json.load(fp)
    except IOError:
        data = []
    
    return data

def get_user_keys():
	config = load_data()
	auth = tweepy.OAuthHandler(config['twitter']['consumer_key'], config['twitter']['consumer_secret'], 'oob')
	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
		print('Error! Failed to get request token.')

	print('visit this authorization url and authorize this bot.')
	print(redirect_url)

	user_pin_input = input('Enter your authorization PIN now:')
	try:
		auth.get_access_token(user_pin_input)
	except tweepy.TweepError:
		print('Error! Failed to get access token.')

	print('Enter your access token in the "config.json":')
	print('access_token: ' + auth.access_token)
	print('access_token_secret: ' + auth.access_token_secret)

get_user_keys()