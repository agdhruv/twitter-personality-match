import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

import tokens # python module that contains my secret keys (for personal reference - go to Twitter and Bluemix dashboards to find secret keys)


# Function to 'flatten' the JSON object that is returned
def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data


# Function to compare traits of two users
def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys] = abs(dict1[keys] - dict2[keys])
    return compared_data


# Main function that gets tweets and sends call to PI API
def analyze(handle):
	# Define all the required keys and tokens to acces the twitter API
	twitter_consumer_key = 'DUB3OZyHj53bDXFLciBD3REhU'
	twitter_consumer_secret = tokens.twitter_consumer_secret
	twitter_access_token = '1159596978-e9JGcGdlc8kDenvOCmAGZ4pKCQDGUETrkCORCPg'
	twitter_access_secret = tokens.twitter_access_secret

	# Create instance of Twitter API
	twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

	# Start making API call
	statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

	# We concatenate all statuses' texts into one large string to send to Watson
	text = ""
	for status in statuses:
		if status.lang == 'en':
			text += status.text.encode('utf-8')

	# Define Personality Insights API credentials
	pi_username = '783d966c-788f-4b4c-b591-e96aebc2fc58'
	pi_password = tokens.pi_password

	# Create instance on Personality Insights API
	pi = PersonalityInsights(username=pi_username, password=pi_password)

	pi_result = pi.profile(text)

	return pi_result


first_handle = "@ATPWorldTour"
second_handle = "@POTUS"

# Analyse
first_traits = analyze(first_handle)
second_traits = analyze(second_handle)

# Flatten
f_first_traits = flatten(first_traits)
f_second_traits = flatten(second_traits)

# Compare and sort
compared_traits = compare(f_first_traits, f_second_traits)
sorted_traits = sorted(compared_traits.items(), key=operator.itemgetter(1))

# Print desired information - top 5 closest personality traits
print "\nTrait -> Difference in percentage shown.\n"
for key, result in sorted_traits[:5]:
	print "{} -> {}".format(key, result)
