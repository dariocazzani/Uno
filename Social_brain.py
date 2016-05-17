from APIs.RedditAPI import RedditAPI
from APIs.TwitterAPI import TwitterAPI
import random
import time
import threading
import json
from APIs import settings

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Social_brain(object):

	def __init__(self):
		# Create twitter object - learn these skills
		self.twitter = TwitterAPI()
		# Create reddit object - learn these skills
		self.reddit = RedditAPI()

		# import knowledge and interests
		self.reddit_topics = self.import_interests('reddit')
		self.twitter_hashtags = self.import_interests('twitter')

	def import_interests(self, source):
		
		print('Loading interests...')
		filename = 'interests.json'
		try:
			with open(filename, 'r') as f:
				interests = json.load(f)
		except Exception as e:
			print('Could not open file %s.\nError was: %s' %(filename, e))
			return []

		# check that source is known
		if source not in interests.keys():
			raise KeyError("Unknown source.\nUno knows from these sources %s" %interests.keys())
			return []
		else:
			return interests[source]

	def add_interests(self, source, subject):
		return

	def show_interests(self):
		print('Loading interests...')
		filename = 'interests.json'
		try:
			with open(filename, 'r') as f:
				interests = json.load(f)
		except Exception as e:
			print('Could not open file %s.\nError was: %s' %(filename, e))
			return []

		for source in interests.keys():
			print('source: %s, interests: %s' %(source, interests[source]))
		return interests

	def post_reddit(self):

		max_trials = 1000

		while True:
			# Post a Reddit
			done = False
			trials = 1
			print('Tweeting from Reddit...')
			while not done and trials <= max_trials:
				next_reddit_topic = self.reddit_topics[random.randint(0, len(self.reddit_topics)-1)]
				print('Next chosen reddit topic: %s' % next_reddit_topic)
				title = []
				link = []
				message = []
				try:
					title, link = self.reddit.get_post(next_reddit_topic)
					print('Title: ' + title)
					print('Url: ' + link)
			
					message = title + ' ' + ' #' + next_reddit_topic + ' ' + link
					
					self.twitter.tweet(message)
					print('Tweeting...')
					done = True
				except Exception as e:
					if not title:
						print('Could not read reddit topic %s.\nError was %s' %(next_reddit_topic, e))
					else:
						print('Could not tweet about ' + title + '\nError was %s' %e)

				trials += 1

			if not done:
				# You gotta do something, we can not find any more reddits!!!!! SHIT!
				self.send_email('No more reddits', 'Help')

			think_time = random.randint(2400, 4800)
			print('I just posted a reddit. Thinking for %d seconds...' % think_time)
			time.sleep(think_time)

	def retweet(self):

		max_trials = 1000

		while True:
			# select a random number of random hastags from the list
			done = False
			trials = 1
			print('Looking for interesting tweets...')
			while not done and trials <= max_trials:
				selected_hashtags = random.sample(self.twitter_hashtags, random.randint(1, len(self.twitter_hashtags)))
				selected_tweet = self.twitter.search_hashtag(selected_hashtags)
				if selected_tweet != -1:				
					try:
						print('Selected hashtags: %s' % str(selected_hashtags))
						#print('selected_tweet: %s' % str(twitter.get_tweet(selected_tweet)))
						self.twitter.retweet(selected_tweet)
						print('Retweeting...')
						done = True
					except Exception as e:
						print('Could not retweet, error was: %s. Trying with an other combination of hashtags' %e)
						pass
				
				trials += 1

			if not done:
				# You gotta do something, we can not find any more tweet!!!!! SHIT!
				self.send_email('No more tweets to retweet', 'Help')
			
			think_time = random.randint(2400, 4800)
			print('I just retweeted, thinking for %d seconds...' % think_time)
			time.sleep(think_time)

	def send_email(self, subject, text):
		server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
		server.starttls()
		server.login(settings.LOGIN_USER, settings.LOGIN_PASSWORD)
		msg = MIMEMultipart()
		msg['From'] = settings.LOGIN_USER
		msg['To'] = settings.MY_EMAIL
		msg['Subject'] = subject
		body = text
		msg.attach(MIMEText(body, 'plain'))
		message = msg.as_string()
		server.sendmail(settings.LOGIN_USER, settings.MY_EMAIL, message)
		server.quit()


if __name__ == "__main__":

	sb = Social_brain()
	thread_reddit = threading.Thread(target=sb.post_reddit)
	thread_reddit.start()

	thread_retweet = threading.Thread(target=sb.retweet)
	thread_retweet.start()

	sb.show_interests()

	thread_retweet.join()
	thread_reddit.join()

		