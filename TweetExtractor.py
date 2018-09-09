from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import re

PicURL = "pic.twitter.com/"
HTTP = "http://"
HTTPS = "https://"
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
ATTRIBUTE = {
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

Base = "https://www.twitter.com/"

class TweetCleaner:
    def __init__(self,tweet):
        self.tweet = tweet
        self.context = tweet.find("div",attrs={"class":"context"})
        self.content =  tweet.find("div",attrs={"class":"content"})
        self.header = self.content.find("div",class_="stream-item-header")
        
    
    def changeTweet(self,tweet):
        self.__init__(tweet)
        
    def get(self,meth): return getattr(self, meth,"Invalid Attribute")()
    def clean_all(self,attributes): 
        for a in attributes:
            attributes[a] = getattr(self, a,"Invalid Attribute")()
        return attributes
    def user_id(self):return self.header.find("a",class_="account-group")["data-user-id"]
    def user_name(self):return self.header.find("a",class_="account-group").find("strong", class_="fullname").text
    def posted(self):return self.header.find("span", class_="_timestamp")["data-time"]
    def tweet_id(self):return self.tweet["data-item-id"]
    def likes(self):return int(self.content.select("span[data-tweet-stat-count]")[2]["data-tweet-stat-count"])
    def replies(self):return int(self.content.select("span[data-tweet-stat-count]")[0]["data-tweet-stat-count"])
    def retweets(self):return int(self.content.select("span[data-tweet-stat-count]")[1]["data-tweet-stat-count"])
    def mentioned_users(self): return [{"name":"@"+a.find("b").text,"iD":a["data-mentioned-user-id"]} for a in self.content.find_all("a",attrs={"class":"twitter-atreply"})]
    def hashtags(self):return ["#"+Hashtag.find("b").text for Hashtag in self.content.find_all("a",attrs={"classs","twitter-hashtag"})]
    def sepLinks(self,S,text,links):
        if S in text:
            Ts = text.split(S)
            text = Ts[0]
            for i in range(1,len(Ts)):
                links.append(S+Ts[i])
        return text,links
    def tweet_data(self):
        tweet = self.content.find("p",class_="TweetTextSize").text
        if tweet is None:
            return TWEET_INFO
        else:
            text,links = self.sepLinks(HTTP,tweet,[])
            text,links =self.sepLinks(HTTP,text,links)
            text,pic_links  = self.sepLinks(PicURL,text,[])
            return {"tweet":tweet,"text":text,"hashtags":self.hashtags(),"mentioned_users":self.mentioned_users(),"links":links,"pic_links":pic_links}

        
    def tweet_info(self):
        info = TWEET_INFO
        if "Pinned Tweet" in self.context.text:
            info["tweet_type"] = "Pinned"
        elif "Retweeted" in self.context.text:
            info["tweet_type"] = "Retweeted"
            info["retweeted_by"] = self.context.find("a")["data-user-id"]
        elif self.context.text == '\n      \n      \n    ':
            info["tweet_type"] = "Normal"
        return info

class Extractor:
    
    def __init__(self,verbose=False):
        self.verbose = verbose
        self.browser = webdriver.Chrome()
        pass
    
    def checkName(self,name):
        resp = requests.get(Base+name)
        if resp.status_code  == 200:
            return True
        elif resp.status_code  == 404:
            return False
        else:
            raise(resp.status_code)

    def extract(self,names,nTweets,attribute=ATTRIBUTE):
        Data = []
        for name in names:
            if self.checkName(name):
                pos = int(0)
                if self.verbose:print("Collecting %s's twitter feed ..."%(name))
                self.browser.get(Base+name)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                while(nTweets > 0):
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    if pos < len(self.browser.page_source):
                        soup = BeautifulSoup(self.browser.page_source[pos:],"html5lib")
                        tweets = soup.find_all("li",{"class":"js-stream-item"})
                        for i in range(min(len(tweets),nTweets)):
                            nTweets -= 1
                            Data.append(TweetCleaner(tweets[i]).clean_all(attribute))
                        pos = len(self.browser.page_source)
                    else:
                        if self.verbose:print("Finished collecting : %d %s Tweets"%(n,name))
                        break
            else:
                raise(ValueError(name+" does not Exist"))
        return Data
