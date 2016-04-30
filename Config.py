twitterKeys = [['your_twitter_access_token_key','your_twitter_access_token_secret','your_twitter_consumer_key','your_twitter_consumer_secret']]

currentTwitter = -1

def getTwitterKeys():
    global currentTwitter
    currentTwitter = (currentTwitter + 1) % len(twitterKeys)
    return twitterKeys[currentTwitter]


fb_access_token = '<your_fb_access_token>'

imgurKeys = [['your_imgur_access_tokenn','your_imgur_refresh_token','your_imgur_client_id','your_imgur_client_secret']]

#for el in imgurKeys:
#   ImgurClient(el[2],el[3]).get_auth_url('token')

currentIMgur = -1

def getImgurKeys():
    global currentIMgur
    currentIMgur = (currentIMgur + 1) % len(imgurKeys)
    return imgurKeys[currentIMgur]
