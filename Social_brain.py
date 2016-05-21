from APIs.RedditAPI import RedditAPI
from APIs.TwitterAPI import TwitterAPI
import random
import time
import threading
import json
from APIs import settings
from datetime import datetime

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

		# get list of current followers
		self.followers = self.twitter.get_followers_list()

	def import_interests(self, source):
		
		print('Loading interests for source %s...' % source)
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
			print('\nSource: %s, \nInterests: %s' %(source, interests[source]))
			print('\n')
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

			think_time = random.randint(20, 40)
			now = datetime.now()
			print('%s - I just posted a reddit. Thinking for %d minutes...' % (now.strftime('%Y/%m/%d %H:%M:%S'), think_time))
			time.sleep(60 * think_time)

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
				
				trials += 1

			if not done:
				# You gotta do something, we can not find any more tweet!!!!! SHIT!
				self.send_email('No more tweets to retweet', 'Help')
			
			think_time = random.randint(20, 40)
			now = datetime.now()
			print('%s - I just retweeted. Thinking for %d minutes...' % (now.strftime('%Y/%m/%d %H:%M:%S'), think_time))
			time.sleep(60 * think_time)

	def find_common_words(self, list1, list2):
		common_words = []
		for word in list1:
			if word in list2:
				common_words.extend(word)
		return common_words

	def send_message_newfriend(self):

		while True:
			new_friends = []
			new_followers_list = []
			try:
				new_followers_list = self.twitter.get_followers_list()
				if new_followers_list:
					new_friends = list(set(new_followers_list) - set(self.followers))
					self.followers = new_followers_list
				else:
					pass
			except Exception as e:
				print('Could not find list of followers.\nError was %s' %e)

			if not new_friends:
				print('No new friends :-(')
			else:
				for friend in new_friends:
					print('Found %d new_friends!' %len(new_friends))
					name, description, screen_name = self.twitter.get_user_info(friend)
					common_interests = self.find_common_words(description.split(), self.twitter_hashtags)
					
					if not common_interests:
						text1 = 'Dear %s, it is great to connect with you!.\nI am glad that we share the same interests.\n' %name
					else:
						common_interests_string = ' '.join(common_interests)
						print('We have these %s interests in common' % common_interests_string)

						text1 = 'Dear %s, it is great to connect with you!.\nI am glad that we share the same interests in %s.\n' %(name, common_interests_string)
					
					text2 = '\nPlease, feel free to add me to LinkedIn if you want to share more insights: no.linkedin.com/in/dariocazzani\n'
					text3 = '\nBest regards and stay in touch.\n'
					text = text1 + text2 + text3
					
					self.twitter.send_message(screen_name, text)

			think_time = random.randint(10, 20)
			now = datetime.now()
			print('%s - Just checked for new friends, doing it again in %d minutes...' % (now.strftime('%Y/%m/%d %H:%M:%S'), think_time))
			time.sleep(60 * think_time) # sleep for a bit

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

	thread_message_newfriend = threading.Thread(target = sb.send_message_newfriend)
	thread_message_newfriend.start()

	sb.show_interests()

	thread_retweet.join()
	thread_reddit.join()

		