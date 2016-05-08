import praw
import os

class RedditAPI:
	def __init__(self, subject):
		
		self.PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
		self.user_agent = ("spiderman2016_0.1")
		self.r = praw.Reddit(user_agent = self.user_agent)
		self.subject = subject
		self.subreddit = self.r.get_subreddit(subject)
		self.filename = self.PROJECT_DIR + '/used_ids.txt'
		
		if os.path.isfile(self.filename):
			with open(self.filename) as f:
				self.used_ids = f.read().splitlines()
		else:
			with open(self.filename, 'w') as f:
				f.write('asdfg\n') # dummy id
				self.used_ids = []

	# return title and url to hottest unseen post
	def get_post(self):
		# get hot 100 and return the one with highest score
		# if not already returned
		score = 0
		for submission in self.subreddit.get_hot(limit = 100):
			if submission.score > score and submission.id not in self.used_ids:
				_id = submission.id
				score = submission.score
				title = submission.title
				link = submission.short_link
			else:
				pass
		# append new id to list of used posts, both file and class variabls
		self.used_ids.append(_id)
		with open(self.filename, 'a') as f:
			f.write(_id + '\n')

		return title, link

if __name__ == "__main__":
	reddit = RedditAPI('python')
	title, link = reddit.get_post()
	print('Title: ' + title)
	print('Url: ' + link)
	title, link = reddit.get_post()
	print('Title: ' + title)
	print('Url: ' + link)