import tweepy
import sys
import settings

class TwitterAPI:
    def __init__(self):
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET
        auth.set_access_token(access_token, access_token_secret)
        
        self.api = tweepy.API(auth)
        self.MAX_LEN = 140

    def tweet(self, message):
        if not isinstance(message, basestring):
            raise TypeError("Tweet must be a string")
        if len(message) > self.MAX_LEN:
            raise ValueError("Tweet must be max %d character len" % self.MAX_LEN)
        try:
            self.api.update_status(status=message)
        except Exception as e:
            print("Could not update status. Error was: %s" % e)


if __name__ == "__main__":    
    
    twitter = TwitterAPI()

    message = 'I like coding bots! A lot!'
    twitter.tweet(message)