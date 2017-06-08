import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

import tokens # python module that contains my secret keys

# Define all the required keys and tokens to acces the twitter API
twitter_consumer_key = 'DUB3OZyHj53bDXFLciBD3REhU'
twitter_consumer_secret = tokens.twitter_consumer_secret
twitter_access_token = '1159596978-e9JGcGdlc8kDenvOCmAGZ4pKCQDGUETrkCORCPg'
twitter_access_secret = tokens.twitter_access_secret


# Create instance of Twitter API
twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

# Start making API call
handle = "@ATPWorldTour"

statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

# Can be used to print all the returned statuses
# for status in statuses:
# 	print status.text

# Prepare API call to Watson
# We concatenate all statuses' texts into one large string to send to Watson

text = ""

for status in statuses:
	if status.lang == 'en':
		text += status.text.encode('utf-8')
