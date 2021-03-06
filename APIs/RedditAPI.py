import praw
import os
import settings

class RedditAPI:

	def __init__(self):
		
		self.PROJECT_DIR = settings.PROJECT_DIR
		self.user_agent = settings.USER_AGENT
		self.r = praw.Reddit(user_agent = self.user_agent)
		self.filename_ids = self.PROJECT_DIR + '/used_ids.ids'
		
		if os.path.isfile(self.filename_ids):
			with open(self.filename_ids) as f:
				self.used_ids = f.read().splitlines()
		else:
			with open(self.filename_ids, 'w') as f:
				f.write('asdfg\n') # dummy id
				self.used_ids = []

	# return title and url to hottest unseen post
	def get_post(self, subject):

		# create subreddit
		subreddit = self.r.get_subreddit(subject)
		# get hot 100 and return the one with highest score
		# if not already returned
		score = 0
		for submission in subreddit.get_hot(limit = 500):
			if submission.score > score and submission.id not in self.used_ids:
				_id = submission.id
				score = submission.score
				title = submission.title
				link = submission.short_link
			else:
				pass
		# append new id to list of used posts, both file and class variabls
		self.used_ids.append(_id)
		with open(self.filename_ids, 'a') as f:
			f.write(_id + '\n')

		return title, link

if __name__ == "__main__":

	reddit = RedditAPI()
	title, link = reddit.get_post('python')
	print('Title: ' + title)
	print('Url: ' + link)
	title, link = reddit.get_post('python')
	print('Title: ' + title)
	print('Url: ' + link)