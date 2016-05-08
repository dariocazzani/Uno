import tweepy
import sys

class TwitterAPI:
    def __init__(self):
        consumer_key = "vZhKYSKqGsnMwiIIXNzHq4UL9"
        consumer_secret = "lQ8POzsOH9nsWoJnp8mmGGLhZsSTSreqEf5fUe9PtnavfOg9aO"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "258817015-fJfHoOwBNe25yJtONxoBNjO8Pv4igpJ5HHapBNYj"
        access_token_secret = "eVUAogOD9whc8KZAyeDbp181WdYHksmL0tCFSXRoWGXhX"
        auth.set_access_token(access_token, access_token_secret)
        
        self.api = tweepy.API(auth)
        self.max_len = 140

    def tweet(self, message):
        if not isinstance(message, basestring):
            raise TypeError("Tweet must be a string")
        if len(message) > self.max_len:
            raise ValueError("Tweet must be max %d character len" % self.max_len)
        try:
            self.api.update_status(status=message)
        except Exception as e:
            print("Could not update status. Error was: %s" % e)


if __name__ == "__main__":    
    
    twitter = TwitterAPI()

    message = 'I like coding bots!'
    twitter.tweet(message)