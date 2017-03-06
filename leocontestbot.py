from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy.auth import OAuthHandler
from tweepy import Stream
import json
import logging
import warnings
from pprint import pprint
import time


#Twitter Auth
CONSUMER_KEY = "yzTBi3zPx8GSSC2v6aXk8HB2q"
CONSUMER_SECRET = "FJzDklPQ8uf0JW9BOpEOnVw5H9PdZKGo9GNGvbrdkhj7JC7noJ"
ACCESS_TOKEN = "838433290310799360-dLWPQM2mNq27o8uBO6VpjYLFO74tTOv"
ACCESS_TOKEN_SECRET = "DgcfQyYs3fV1sAvznfib51wad4Uil5ZuzcTP8ixa1C7PT"
auth_handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_handler.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitter_client = API(auth_handler)
logger = logging.getLogger("Bot")

print "Starting stream listener"
class MyStreamListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        
        try:
                print "Trying to retweet..."
                twitter_client.retweet(tweet['id'])
                print "Done retweeting"
                #print tweet['screen_name']
                print "Trying to favorite..."
                twitter_client.create_favorite(tweet['id'])
                print "Done favoriting"

                print "Trying to follow user..."
                status = twitter_client.get_status(tweet['id'])
                author = status.author
               # print author
                print author.screen_name
                #print author['screen_name']
                #twitter_client.create_friendship(author['screen_name'])
                twitter_client.create_friendship(author.screen_name.encode('utf-8'))
                print "Done following user"

                logging.debug("RT: {}".format(tweet['text']))
 
        except Exception as ex:
            print ex
 
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            print "Status code 420 error... blaze that motherfucker"
            return False

while(True):
    try:
        myStreamListener = MyStreamListener()
        myStream = Stream(auth = twitter_client.auth, listener=myStreamListener)
        myStream.filter(track=['follow contest retweet', 'giveaway contest follow retweet'])
    except Exception as e:
        print e
    print "Waiting 300 seconds..."
    time.sleep(100)
    print "Waiting 200 seconds..."
    time.sleep(100)
    print "Waiting 100 seconds..."
    time.sleep(100)
    print "Retrying to find more tweets"

