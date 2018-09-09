from bs4 import BeautifulSoup
import requests
import time
import re

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

ATTR = [ "tweet_id","user_id" ,"user_name","posted","tweet","tweet_type","retweeted_by","replies","likes","retweets"]
Base = "https://www.twitter.com/"

class TweetCleaner:
    def __init__(self,tweet):
        self.T = tweet
        self.context = tweet.find("div",attrs={"class":"context"})
        self.content =  tweet.find("div",attrs={"class":"content"})
        self.header = self.content.find("div",class_="stream-item-header")
        
    
    def changeTweet(self,tweet):
        self.__init__(tweet)
        
    def get(self,meth): return getattr(self, meth,"Invalid Attribute")()
    def clean_all(self,attributes): 
        attrs = {}
        for a in attributes:
            attrs[a] = getattr(self, a,"Invalid Attribute")()
        return attributes
    def user_id(self):return self.header.find("a",class_="account-group")["data-user-id"]
    def user_name(self):return self.header.find("a",class_="account-group").find("strong", class_="fullname").text
    def posted(self):return self.header.find("span", class_="_timestamp")["data-time"]
    def tweet_id(self):return self.T["data-item-id"]
    def likes(self):return int(self.content.select("span[data-tweet-stat-count]")[2]["data-tweet-stat-count"])
    def replies(self):return int(self.content.select("span[data-tweet-stat-count]")[0]["data-tweet-stat-count"])
    def retweets(self):return int(self.content.select("span[data-tweet-stat-count]")[1]["data-tweet-stat-count"])
    def mentioned_users(self): return [{"name":"@"+a.find("b").text,"iD":a["data-mentioned-user-id"]} for a in self.content.find_all("a",attrs={"class":"twitter-atreply"})]
    def hashtags(self):return ["#"+Hashtag.find("b").text for Hashtag in self.content.find_all("a",attrs={"classs","twitter-hashtag"})]
    def sepLinks(self,Str,text,links):
        Ts = text.split(Str)
        for i in range(1,len(Ts)):
            links.append(Str+Ts[i])
        return Ts[0],links
    def tweet(self):
        tweet = self.content.find("p",class_="TweetTextSize").text
        if tweet is None:
            return TWEET
        text,links = self.sepLinks("https://",tweet,[])
        text,links =self.sepLinks("http://",text,links)
        text,pic_links  = self.sepLinks("pic.twitter.com/",text,[])
        return {"tweet":tweet,"text":text,"hashtags":self.hashtags(),"mentioned_users":self.mentioned_users(),"links":links,"pic_links":pic_links}
    
    def retweeted_by(self):
        try:
            self.context.find("a")["data-user-id"]
        except:
            return None
    def tweet_type(self):
        if "Pinned Tweet" in self.context.text:return "Pinned"
        elif "Retweeted" in self.context.text:return "Retweeted"
        elif "\n      \n      \n    " == self.context.text: return "Normal"
        else: return None


class Tweets:
    
    def __init__(self,browser,verbose=False):
        self.verbose = verbose
        self.browser = browser
        pass
    
    def checkName(self,name):
        resp = requests.get(Base+name)
        if resp.status_code  == 200:
            return True
        elif resp.status_code  == 404:
            return False
        else:
            raise(resp.status_code)

    def extract(self,names,nTweets=20000,attributes=None):
        if attributes is None: attributes = ATTR
        Data = []
        for name in names:
            if self.checkName(name):
                pos = int(0)
                if self.verbose:print("Collecting %s's twitter feed ..."%(name))
                self.browser.get(Base+name)
                while(nTweets > 0):
                    self.scroll()
                    time.sleep(2)
                    if pos < len(self.browser.page_source):
                        soup = BeautifulSoup(self.browser.page_source[pos:],"html5lib")
                        tweets = soup.find_all("li",{"class":"js-stream-item"})
                        for i in range(min(len(tweets),nTweets)):
                            nTweets -= 1
                            Data.append(TweetCleaner(tweets[i]).clean_all(attributes))
                        pos = len(self.browser.page_source)
                    else:
                        if self.verbose:print("Finished collecting : %d %s Tweets"%(n,name))
                        break
            else:
                raise(ValueError(name+" does not Exist"))
        return Data

    def scroll(self):
         self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def done(self):
        self.browser.close()