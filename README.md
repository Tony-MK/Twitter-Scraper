# TwitterExtractor

A simple to use webscarper to collect the tweets of a user in python.

## Installing
Open CMD and run the follwing commands ...

`git clone https://github.com/zana-Afrika/TwitterExtractor`

`pip install ./TwitterExtractor`

## Usage
```python


from TwitterExtractor import Extractor
ex = Extractor.TweetExtractor(verbose=False)
names = ["bitcoin","billgates","elonmusk"]

attributes = {"user_id":"","tweet_data":"","likes":""}

# attributes is by default ATTRIBUTES, if not passed it returns all attributes
tweets = ex.extract(names=names,nTweets=2,attributes=attributes)

for tweet in tweets:
  print(tweet["user_id"])# prints user's id 
  print(tweet["tweet_data"].["tweet"])# prints raw tweet
  print(tweet["tweet_data"].["text"])# prints cleaned version of the tweet
  print(tweet["tweet_data"].["likes"])# prints number of likes
  print(tweet["tweet_data"].["hashtags"])# prints hashtags
  
```
## Attributes

```python

TWEET_DATA = {
        "tweet":None,
        "text":None,
        "hashtags":None,
        "mentioned_users":None,
        "links":None,
        "pic_links":None
}
TWEET_INFO = {
        "tweet_type":None,
        "retweeted_by":None
}
ATTRIBUTES = {
        "user_id": None,
        "user_name":None,
        "posted": None,
        "tweet_id":None,
        "tweet_data":None,
        "tweet_info":None,
        "replies":None,
        "likes":None,
        "retweets":None
            
}

```

## NOTE: Still in development
