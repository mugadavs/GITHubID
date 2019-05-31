import requests
import json
import logging
import sys

class API(object):

	def __init__(self):
		self.base_url = "https://api.github.com/users/"

	# Get single follower data #
	def get_follower_data(self, user):
		try:
			followers = requests.get(user['followers_url']+"?per_page=5")
			return json.loads(followers.content)
		except Exception as e:
			logging.error(e)

	# Returns Followers #
	def get_followers(self, userid):
	    url = self.base_url+"%s/followers?per_page=5"%userid
	    try:
			data = requests.get(url)
			if data.status_code == 200:
				response_data = json.loads(data.content)
				if 'message' not in response_data:
				    for resp in response_data:
				    	resp['followers'] = self.get_follower_data(resp)
				    	for k in resp['followers']:
				    		k['followers'] = self.get_follower_data(resp)
				    return json.dumps(response_data)
				else:
					return response_data
			else:
				return json.loads(data.content)
	    except Exception as e:
	    	logging.error(e)

	# Get single repository #
	def get_repo_data(self, user):
		try:
			repo = requests.get(user['repos_url']+"?per_page=3")
			return json.loads(repo.content)
		except Exception as e:
			logging.error(e)

	# Get single stargazer #
	def get_stargazers_data(self, user):
		try:
			stargazers = requests.get(user['stargazers_url']+"?per_page=3")
			return json.loads(stargazers.content)
		except Exception as e:
			logging.error(e)

	# Return Repositories and Stargazers data
	def get_repos(self, userid):
		try:
			repos_url = self.base_url+"%s/repos?per_page=3"%userid
			repos_data = requests.get(repos_url)
			if repos_data.status_code == 200:
				response_data = json.loads(repos_data.content)
				if 'message' not in response_data:
					for resp in response_data:
						resp['repos'] = self.get_repo_data(resp)
						resp['stargazers'] = self.get_stargazers_data(resp)
						if resp['repos']:
							for rep in resp['repos']:
								rep['repos'] = self.get_repo_data(resp)
						if resp['stargazers']:		
							for k in resp['stargazers']:
								k['stargazers'] = self.get_stargazers_data(resp)
					return json.dumps(response_data)
				else:
					return response_data
			else:
				return json.loads(repos_data.content)
		except Exception as e:
			logging.error(e)


if __name__ == '__main__':
	logger = logging.getLogger('__name__')
	logging.basicConfig(level=logging.DEBUG)
	logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')
	stdhanlder = logging.StreamHandler(sys.stdout)
	stdhanlder.setFormatter(logFormatter)
	logger.addHandler(stdhanlder)
	githubid = raw_input('Enter Your githubid:')
	inst = API()
	followers = inst.get_followers(githubid)
	repos = inst.get_repos(githubid)
	#print followers
	#print "******************************************"
	#print repos



