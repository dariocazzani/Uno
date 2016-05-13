import tweepy
import sys
import settings
import random
import os
import time

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

        self.PROJECT_DIR = settings.PROJECT_DIR
        self.filename_ids = self.PROJECT_DIR + '/used_tweets.ids'
        if os.path.isfile(self.filename_ids):
            with open(self.filename_ids) as f:
                self.used_tweets = f.read().splitlines()
        else:
            with open(self.filename_ids, 'w') as f:
                f.write('asdfg\n') # dummy id
                self.used_tweets = []

    def tweet(self, message):

        if not isinstance(message, basestring):
            raise TypeError("Tweet must be a string")
        if len(message) > self.MAX_LEN:
            raise ValueError("Tweet must be max %d character len" % self.MAX_LEN)
        try:
            self.api.update_status(status=message)
        except Exception as e:
            print("Could not update status. Error was: %s" % e)

    """
    For a complete description on how to formulate queries:
    https://dev.twitter.com/rest/public/search
    """
    def search_hashtag(self, hashtags):
        for h in hashtags: # hastags is a list
            if not isinstance(h, basestring):
                raise TypeError("hashtag must be a string")
            if not h[0] == '#':
                raise TypeError("hashtag must begin with #")
            if len(h) < 2 or len(h) > 30:
                raise ValueError("hashtag must be at least 1 character long and less than 30")

        query = ' '.join(hashtags)
        max_tweets = 300
        searched_tweets = []
        try:
            searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query, 
                                result_type="recent", lang="en").items(max_tweets)]
        except Exception as e:
            print('Could not search tweets, error was %s, possibly too many requests.\nSleeping for 5 minutes...' %e)
            time.sleep(300)
        # if no result, pop one hashtag and try again
        while len(searched_tweets) == 0:
            if not hashtags: 
                return -1
            else:
                hashtags.pop(random.randint(0, len(hashtags) - 1))
                try:
                    searched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query, 
                                result_type="recent", lang="en").items(max_tweets)]
                except Exception as e:
                    print('Could not search tweets, error was %s, possibly too many requests.\nSleeping for 5 minutes...' %e)
                    time.sleep(300) 

        status = 0
        # select one tweet that has not been searched before
        for st in searched_tweets:
            if str(st.id) not in self.used_tweets:
                status = st.id
                # append new id to list of used tweets, both file and class variables
                self.used_tweets.append(str(status))
                with open(self.filename_ids, 'a') as f:
                    f.write(str(status) + '\n')
                return status
            else:
                pass
        
        return -1

    def remove_id_from_list(self, _id):
        """
        implement a function that given an id, removes that tweet from the used_tweet file so
        that it can be used (again)
        """
        return

    def retweet(self, _id):
        # check that it is an int
        self.api.retweet(_id)

    def get_tweet(self, _id):
        tweet = self.api.get_status(_id)
        return tweet.text
 


if __name__ == "__main__":    
    
    twitter = TwitterAPI()

    message = 'I like coding bots! A lot!'
    twitter.tweet(message)