import tweepy
import datetime
from time import sleep
import logging

def create_api():
    API_key     = 'ZCvwUxlgRmfst9AlNYuxHo6Ej'
    API_key_s   = 'ZFCSAYK6iavj6uYrVFiy9DVnzJ88ZUh4K5UrKCkbxsy0HwRWyy'
    acess_tkn   = '1295488730548051969-GcNl7WsBw1wpIc8zXNLermjpQq291u'
    acess_tkn_s = 'ehhLXURUNyWQa20Fid2GmUixzLvOSmFBVnYYOo1mI1jhD'

    auth = tweepy.OAuthHandler(API_key, API_key_s)

    auth.set_access_token(acess_tkn, acess_tkn_s)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except Exception as e:
        logging.error('Error creating API', exc_info=True)
        raise e
    logging.info('API created')

    return api

def check_mentions(api, since_id):
    logging.info('Retrieving mentions')
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        
        logging.info(f'Answering to {tweet.user.name}')

        if not tweet.user.following:
            tweet.user.follow()
        try:
            api.update_status(status=f'Olá {tweet.user.name} ainda estou em testes, não sei responder muita coisa.',
                              in_reply_to_status_id=tweet.id,
                              auto_populate_reply_metadata=True)

        except tweepy.TweepError as e:
            if e.api_code == 187:
                print('Duplicated message')
            else:
                raise error

    return new_since_id

def main():        
    api = create_api()

    while True:
        arq = open('since_id.txt', 'r')

        for line in arq:
            since_id = int(line)

        arq.close()

        since_id = check_mentions(api, since_id)
        
        arq = open('since_id.txt', 'w')

        arq.write(str(since_id))

        arq.close()

        logging.info('Waiting...')
        sleep(60)

if __name__ == '__main__':
    main()