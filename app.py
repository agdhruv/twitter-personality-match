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



