import methods
import os

def main():
    config = methods.load_data('{}/config_example.json'.format(os.getcwd()))

    data = methods.get_monthly_history(config['address'], 'DFI', 'UtxosToAccount', 1000)
    datafilePath = '{}/data.json'.format(os.getcwd())
    prevData = methods.load_data(datafilePath)
    methods.save_data(datafilePath, data)
    diff = methods.get_diff(data, prevData)
    message = methods.get_message(diff, config['address'], config['tweet_settings']['base_text_monthly'], config['tweet_settings']['include_defiscan_link'])

    if config['verbose'] and len(message) > 0:
        print('will tweet message:\n' + message)

    if config['send_tweet'] and len(message) > 0:
        methods.send_tweet(message, config)
        print('tweet sent with message\n'+message)


if __name__ == "__main__":
    main()
