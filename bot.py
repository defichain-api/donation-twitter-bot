import requests
import json
import tweepy
import os

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
    larger_set = utxo if len(utxo) > len(token) else token
    smaller_set = token if len(token) < len(utxo) else utxo

    for k, v in smaller_set.items():
        if k in larger_set:
            larger_set[k]['amount'] += v['amount']
        else:
            larger_set[k]['amount'] = v['amount']

    return larger_set


def load_data(datafile):
    try:
        with open(datafile, 'r') as fp:
            prevData = json.load(fp)
    except IOError as e:
        print(e)
        prevData = {}
    
    return prevData


def save_data(datafile, data):
    # Store into tmp file
    with open(datafile, 'w+') as f:
        json.dump(data, f)


def get_diff(new, old):
    retval = []
    for k, v in new.items():
        # hide LM tokens (format: TOKEN_A-TOKEN_b, e.g. BTC-DFI)
        if k.find('-') != -1:
            continue
        if k in old:
            if v['amount'] > old[k]['amount']:
                difference = v['amount'] - old[k]['amount']
                if k == 'DFI' and difference < 1:
                    print('DFI amount below 1, skipping: {:.8f}'.format(difference))
                    continue
                retval.append((k, difference))
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
        if len(message) > 0:
            api.update_status(status=message)
    except tweepy.errors.TweepyException as e:
        print(e)
        print('error while sending the tweet...')


def main():
    config = load_data('{}/config.json'.format(os.getcwd()))

    dataToken = parse_ocean_token(config['address'])
    dataUTXO = parse_ocean_utxo(config['address'])
    data = merge_token_utxo(dataUTXO, dataToken)
    datafilePath = '{}/data.json'.format(os.getcwd())
    prevData = load_data(datafilePath)
    save_data(datafilePath, data)
    diff = get_diff(data, prevData)
    message = get_message(diff, config['address'], config['tweet_settings']['base_text'], config['tweet_settings']['include_defiscan_link'])

    if config['verbose'] and len(message) > 0:
        print('will tweet message:\n' + message)

    if config['send_tweet'] and len(message) > 0:
        send_tweet(message, config)
        print('tweet sent with message\n'+message)


if __name__ == "__main__":
    main()
