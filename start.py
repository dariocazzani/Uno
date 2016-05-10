from APIs.RedditAPI import RedditAPI
from APIs.TwitterAPI import TwitterAPI
import random
import time

# list of interesting reddit topics
reddit_topics = ['Python',
			'deeplearning',
			'machinelearning',
			'Matlab',
			'TensorFlow',
			'NeuralNetworks']

# create twitter object
twitter = TwitterAPI()
# create reddit object
reddit = RedditAPI()

if __name__ == "__main__":

	while True:
		done = False
		while not done:
			next_reddit_topic = reddit_topics[random.randint(0, len(reddit_topics)-1)]
			print('Next chosen reddit topic: %s' % next_reddit_topic)
			try:
				title, link = reddit.get_post(next_reddit_topic)
				print('Title: ' + title)
				print('Url: ' + link)
			except Exception as e:
				print('Could not read topic, error was %s' % e)

			# create tweet
			message = title + ' ' + ' #' + next_reddit_topic + ' ' + link
			try:
				twitter.tweet(message)
				print('Tweeting...')
				done = True
			except:
				pass

		time.sleep(random.randint(1200, 360))

