import os 
os.environ['PYTHONASYNCIODEBUG'] = '1'
import tweepy
import pandas as pd
import to_database as db
from decouple import config as c
import logging
logging.basicConfig(level=logging.INFO)

auth = tweepy.OAuthHandler(c('TWITTER_API_KEY'), c('TWITTER_API_SECRET'))   
auth.set_access_token(c('TWITTER_ACCESS_TOKEN'), c('TWITTER_ACCESS_TOKEN_SECRET')) 

account = str(input('Ingrese el nombre de una cuenta de twitter sin @: '))
count = int(input('Ingrese la cantidad de tweets requeridos: '))

api = tweepy.API(auth)
tweets = api.user_timeline(screen_name='@{}'.format(account), 
                        count=count,
                        include_rts = False,
                        tweet_mode = 'extended',
                        )

tweets_list = []

for tweet in tweets:
    text = tweet._json['full_text']

    refined_tweet = {'username': tweet.user.screen_name,
                     'text': text,      
                     'favorite_count': tweet.favorite_count,
                     'retweet_count': tweet.retweet_count,
                     'created_at': tweet.created_at,
                     'id_str': tweet.id_str
                    }

    tweets_list.append(refined_tweet)

df = pd.DataFrame(tweets_list)

df.to_csv('./data/{}_data_tweets.csv'.format(account)) 

db.load_data('./data/{}_data_tweets.csv'.format(account),account)

os.remove('./data/{}_data_tweets.csv'.format(account))

logging.info('El proceso fue realizado correctamente!')

