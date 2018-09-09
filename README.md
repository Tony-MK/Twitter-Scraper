# TwitterExtractor

A simple to use webscarper to collect the tweets of a user in python.

## Installing
Open CMD and run the follwing commands ...

`git clone https://github.com/zana-Afrika/TwitterExtractor`

`pip install ./TwitterExtractor`

## Usage
```python

from selenium import webdriver
#Choose a browser eg.Chrome, FireFox,Safari
browser = webdriver.Chrome()

from TwitterExtractor import Tweets
# Create a Tweet Extractor 
ex = Tweets(browser=browser,verbose=False)

#List Names of users to collect data
names = ["bitcoin","billgates","elonmusk"]

#Attributes to return 
attributes = {"user_id","tweet_data":""}

# attributes is by default None, if not passed it returns all attributes
tweets = ex.extract(names=names,nTweets=2,attributes=attributes)

for tweet in tweets:
  print(tweet["user_id"])# prints user's id 
  print(tweet["tweet_data"].["tweet"])# prints raw tweet
  print(tweet["tweet_data"].["text"])# prints cleaned version of the tweet
  print(tweet["tweet_data"].["likes"])# prints number of likes
  print(tweet["tweet_data"].["hashtags"])# prints hashtags

ex.close()
```
## Attributes

```python

TWEET = {
    "tweet":None,
    "text":None,
    "hashtags":None,
    "mentioned_users":None,
    "links":None,
    "pic_links":None
}
ATTRIBUTES = {
        "tweet_id":None,
        "user_id": None,
        "user_name":None,
        "posted": None,
        "tweet":TWEET,

        "tweet_type":None,
        "retweeted_by":None,

        "replies":None,
        "likes":None,
        "retweets":None
}

```

## NOTE: Still in Beta
