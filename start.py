from APIs.RedditAPI import RedditAPI
from APIs.TwitterAPI import TwitterAPI
import random
import time

# list of interesting topics
topics = ['python',
			'deeplearning',
			'machinelearning',
			'matlab']

# create list of reddits, one for topic
reddit_list = []
for topic in topics:
	reddit_list.append(RedditAPI(topic))

# create twitter object
twitter = TwitterAPI()

if __name__ == "__main__":

	while True:
		time.sleep(100)

		done = False
		while not done:
			next_topic = random.randint(0, len(reddit_list)-1)
			print('Next chosen topic: %s' % topics[next_topic])
			try:
				title, link = reddit_list[next_topic].get_post()
				print('Title: ' + title)
				print('Url: ' + link)
			except:
				pass

			# create tweet
			message = title + ' ' + link
			try:
				twitter.tweet(message)
				done = True
			except:
				pass

