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

# list of interesting hastags
twitter_hastags = ['#datascience',
					'#MachineLearning',
					'#NeuralNetworks',
					'#AI',
					'#TensorFlow',
					'#Python',
					'#RecurrentNeuralNetworks',
					'#bigdata',
					'#NLP',
					'#NatualLanguageUnderstanding',
					'#NLU',
					'#SyntaxNet',
					'#raspberrypi'
					]

# create twitter object
twitter = TwitterAPI()
# create reddit object
reddit = RedditAPI()

if __name__ == "__main__":

	# to be done as self:
	max_trials = 1000

	
	while True:
		# Post a Reddit
		done = False
		trials = 1
		while not done and trials <= max_trials:
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
			trials += 1

		if not done:
			# You gotta do something, we can not find any more reddits!!!!! SHIT!
			pass

		#think_time = random.randint(600, 1200)
		#print('Thinking for %d seconds...' % think_time)
		#time.sleep(think_time)


		# retweet an interesting tweet

		# select a random number of random hastags from the list

		done = False
		trials = 1
		while not done and trials <= max_trials:
			selected_hashtags = random.sample(twitter_hastags, random.randint(1, len(twitter_hastags)))
			selected_tweet = twitter.search_hashtag(selected_hashtags)
			if selected_tweet != -1:				
				try:
					print('Selected hashtags: %s' % str(selected_hashtags))
					#print('selected_tweet: %s' % str(twitter.get_tweet(selected_tweet)))
					twitter.retweet(selected_tweet)
					print('Retweeting...')
					done = True
				except Exception as e:
					print('Could not retweet, error was: %s. Trying with an other combination of hashtags' %e)
					pass
			
			trials += 1

		if not done:
			# You gotta do something, we can not find any more tweet!!!!! SHIT!
			pass
		
		think_time = random.randint(600, 1200)
		print('Thinking for %d seconds...' % think_time)
		time.sleep(think_time)
