from APIs.RedditAPI import RedditAPI
from APIs.TwitterAPI import TwitterAPI
import random
import time

# list of interesting topics
topics = ['python',
			'deeplearning',
			'machinelearning',
			'matlab']

# create twitter object
twitter = TwitterAPI()
# create reddit object
reddit = RedditAPI()

if __name__ == "__main__":

	while True:
		done = False
		while not done:
			next_topic = topics[random.randint(0, len(reddit_list)-1)]
			print('Next chosen topic: %s' % next_topic)
			try:
				title, link = reddit_list[next_topic].get_post(next_topic)
				print('Title: ' + title)
				print('Url: ' + link)
			except:
				pass

			# create tweet
			message = title + ' ' + link
			try:
				twitter.tweet(message)
				print('Tweeting...')
				done = True
			except:
				pass

		time.sleep(3600)

