from TwitterAPI import TwitterAPI
from Status import Status
import re
import Config

def validTweet(text):
    t = re.sub('@[^\s]+','',text,flags=re.MULTILINE)
    t = re.sub('[^a-zA-Z]','',t)
    if len(t) > 5:
        return True
    return False

def fetch_profile(user):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    api = TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret)
    profile = api.fetch_user_profile(user.twitterId)
    user.twitterFollower = profile['followers_count']
    user.twitterName = profile['name']
    user.twitterImageURL = profile['profile_image_url'].replace('_normal','')
    return user

def getTweets(user,clean=True,includeRetweets=False,maxTweets=1000000,includeOtherMentions=True):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    api = TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret)

    tweets = []
    li = api.fetch_by_user_names(user.twitterId,clean = clean)
    
    while li is not None and len(li) > 0:
        if "errors" in li and li["errors"][0]["code"] == 88:
            return []
        for tweet in li:
            tweetText = str(tweet['text'].encode("utf-8")).replace('\\n', ' ').replace('\\r', '').strip()[2:-1]
            if not includeRetweets and tweetText.startswith('RT'):
                continue
            if not includeOtherMentions and "@" in tweet['text']:
                continue
            if clean:
                tweetText = re.sub(r'https?:\/\/[^\s]*','',tweetText, flags=re.MULTILINE)
                tweetText = re.sub(r'\\x..','',tweetText, flags=re.MULTILINE)
                tweetText = re.sub(r'&amp;','and',tweetText, flags=re.IGNORECASE)
                tweetText = re.sub(r'[\s\t]+',' ',tweetText, flags=re.IGNORECASE)
                tweetText.replace('#','')
                tweetText = re.sub('^\s*rt\s',' ',tweetText,flags=re.IGNORECASE)
                if not validTweet(tweetText):
                    continue
                
            st = Status()
            st.id = tweet['id']
            st.likes = tweet['favorite_count']
            st.shares = tweet['retweet_count']
            st.CreatedOn = tweet['created_at']
            st.statusType = 1
            st.statusText = tweetText
            st.language = tweet["lang"]

            tweets.append(st)
        minId = min(tweets,key=lambda p:p.id).id
        li = api.fetch_by_user_names(user.twitterId,id= minId - 1,clean = clean)
        if len(tweets) > maxTweets or li is None or len(li) < 10:
            break
    return tweets

def getMentions(term,since=''):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    api = TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret)
    obj = api.fetch_by_terms(term,since)
    return obj

def postUpdate(status,media=None):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    return TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret).post_update(status,media)

def favouriteTweet(tweetId):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    return TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret).favourite_post(tweetId)

def reTweet(tweetId):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    return TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret).reTweet_post(tweetId)

def getFollowers(user):
    twitter_access_token_key,twitter_access_token_secret,twitter_consumer_key,twitter_consumer_secret = Config.getTwitterKeys()
    api = TwitterAPI(twitter_access_token_key,twitter_access_token_secret, twitter_consumer_key, twitter_consumer_secret)

    followers = []
    print(user.twitterId + '...')
    followers_json = api.fetch_followers_list(user.twitterId)
    if "errors" in followers_json and followers_json["errors"][0]["code"] == 88:
        return []
    followers.extend(followers_json['users'])
    next_cursor = followers_json['next_cursor']
    while next_cursor > 0:
        followers_json = api.fetch_followers_list(user.twitterId,cursor=next_cursor)
        if "errors" in followers_json and followers_json["errors"][0]["code"] == 88:
            return followers
        followers.extend(followers_json['users'])
        next_cursor = followers_json['next_cursor']
    return followers

def main():
    # who i follow
    from User import User
    user = User()
    user.twitterId = "social_visualiz" 
    followers = set([follower['screen_name'] for follower in getFollowers(user)])

    if len(followers) == 0:
        raise "ERROR!!"

    prev_followers = None
    with open('WhoIFollow.txt') as f:
        prev_followers = f.readlines()
    prev_followers = set([x.strip().lower() for x in prev_followers])
    
    #already requested
    requested = []
    with open('customRequest.txt') as f:
        requested = f.readlines()
    from Handler import getSelfRequest
    requested = set([getSelfRequest(x.strip())['target'].lower() for x in requested])

    #request completed
    completed = []
    with open('usersDone.txt') as f:
        completed = f.readlines()
    completed = set([el.strip().split()[0].lower() for el in completed])

    print("already_requested:" + str(len(requested)))
    print("already_completed:" + str(len(completed)))
    print("prev_followers:" + str(len(prev_followers)))
    print("followers:" + str(len(followers)))

    #update
    with open("customRequest.txt", "a") as myfile2:
        with open("WhoIFollow.txt", "a") as myfile:
            for screen_name in followers:
                if screen_name.lower() not in prev_followers:
                    myfile.write(screen_name + '\n')
                if screen_name.lower() not in requested and screen_name.lower() not in completed:
                    myfile2.write("@social_visualiz #wordcloud @" + screen_name + '\n')

if __name__ == "__main__":
    main()