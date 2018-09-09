from TwitterExtractor import Tweets
from selenium import webdriver

# Choose a browser eg.Chrome, FireFox,Safari
browser = webdriver.Chrome()

# Create a Tweet Extractor 
EX = Tweets(browser=browser,verbose=False)

# List Names of users to extract tweets from 
names = ["bitcoin","billgates","elonmusk"]

# Attributes to extract. If not passed or None by default it returns all attributes 
attributes = ["user_id","tweet_type","posted","tweet","replies","likes"]

# Number of tweets to extract per user
nTweets= 1

#Extract Tweet data 
tweets = EX.extract(names=names,nTweets=nTweets,attributes=attributes)

for user in tweets:
  print(tweets[user][0]["tweet_type"]) # prints either PINNED, RETWEETED or NORMAL
  print(tweets[user][0]["user_id"])# prints user's id
  print(tweets[user][0]["posted"])# prints time posted as UNIX 
  print(tweets[user][0]["likes"])# prints number of likes
  print(tweets[user][0]["replies"])# prints number of likes

  tweet = tweets[user][0]["tweet"]
  print(tweet["tweet"])# prints raw version of the tweet
  print(tweet["text"])# prints cleaned version of the tweet
  print(tweet["hashtags"])# prints hashtags
  print(tweet["mentioned_users"])# prints mentioned users
  print(tweet["links"])# prints links found
  print(tweet["pic_links"])# prints twitter hosted picture links found

# Closes the browser window
EX.done()