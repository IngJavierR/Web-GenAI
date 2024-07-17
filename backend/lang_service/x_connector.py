import tweepy
import os
from dotenv import load_dotenv

load_dotenv()
# Credenciales de la API de Twitter
consumer_key = os.environ.get('X_CONSUMER_KEY')
consumer_secret = os.environ.get('X_CONSUMER_SECRET')
access_token = os.environ.get('X_ACCESS_TOKEN')
access_token_secret = os.environ.get('X_ACCESS_TOKEN_SECRET')

# Autenticación con Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)


def send_tweet(tweet, image_path=None):

    if image_path:
        print('Se envía tweet con imagen')
        media = api.media_upload(image_path)
        client.create_tweet(text=tweet, media_ids=[media.media_id])
    else:
        print('Se envía tweet sin imagen')
        client.create_tweet(text=tweet)