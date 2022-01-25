from audioop import add
from sys import argv
import requests
import json
import tweepy

def parse_ocean_token(address):
    retval = {}
    request = requests.get(f'https://ocean.defichain.com/v0/mainnet/address/{address}/tokens')
    request.raise_for_status()

    if not request.ok:
        exit(f'Error {request.status_code} in token request')

    for i in request.json()['data']:
        retval[i['symbol']] = {
            'symbol': i['symbol'],
            'symbolKey': i['symbolKey'],
            'amount': float(i['amount'])
        }

    return retval

def parse_ocean_utxo(address):
    retval = {}
    request = requests.get(f'https://ocean.defichain.com/v0/mainnet/address/{address}/balance')
    request.raise_for_status()

    if not request.ok:
        exit(f'Error {request.status_code} in utxo request')

    retval['DFI'] = {
        'symbol': 'DFI',
        'symbolKey': 'DFI',
        'amount': float(request.json()['data'])
    }

    return retval

def merge_token_utxo(utxo, token):
    mergedData = token.copy()
    if 'DFI' in utxo.keys():
        mergedData.update({'DFI': {'symbol': 'DFI', 'symbolKey': 'DFI', 'amount': utxo['DFI']['amount'] + token['DFI']['amount']}})
    else:
        mergedData.append(token)

    return mergedData

def load_data(datafile):
    try:
        with open(datafile, 'r') as fp:
            prevData = json.load(fp)
    except IOError:
        prevData = []
    
    return prevData

def save_data(datafile, data):
    # Store into tmp file
    with open(datafile, 'w+') as f:
        json.dump(data, f)

def get_diff(new, old):
    retval = []
    for k, v in new.items():
        if k in old:
            if v['amount'] > old[k]['amount'] and v['amount'] - old[k]['amount'] > 1:
                retval.append((k, v['amount'] - old[k]['amount']))
        else:
            retval.append((k, v['amount']))
    return retval

def get_message(diff, address, base_text, include_defiscan_link):
    message = ''
    if len(diff) > 0:
        message = base_text + '\n'
        for coin, amount in diff:
            message += f'{amount:.8f} {coin}\n'

        if include_defiscan_link:
            message += '\nsee all details: https://defiscan.live/address/' + address

    return message

def twitter_client(config):
    auth = tweepy.OAuthHandler(config['twitter']['consumer_key'], config['twitter']['consumer_secret'])
    auth.set_access_token(config['twitter']['access_token'], config['twitter']['access_token_secret'])
    
    return tweepy.API(auth)

def send_tweet(message, config):
    api = twitter_client(config)
    try:
        api.update_status(message)
    except tweepy.TweepError:
        print('error while sending the tweet...')


def main():
    config = load_data('config.json')

    dataToken = parse_ocean_token(config['address'])
    dataUTXO = parse_ocean_utxo(config['address'])
    data = merge_token_utxo(dataUTXO, dataToken)
    prevData = load_data(config['datafile'])
    save_data(config['datafile'], data)
    diff = get_diff(data, prevData)

    if config['verbose']:
        print(get_message(diff, config['address'], config['tweet_settings']['base_text'], config['tweet_settings']['include_defiscan_link']))

    if config['send_tweet']:
        send_tweet(get_message(diff, config['address']), config)

if __name__ == "__main__":
    main()
