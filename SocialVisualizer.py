import TwitterHelper as th
import FacebookHelper as fh
from User import User
from Visualizer import Visualizer
from KeyBoardHeatMap import createKeyBoardHeatMap

from wordcloud import STOPWORDS
from nltk.corpus import stopwords

from PIL import Image
from io import BytesIO
import requests
import re

global_stopwords = {}

class SocialVisualizer:
    def __init__(self,twitterId,facebookId='',customImagePath=None, customStopWords=None,bgColor="black",textColor="multi",maxTweets=10000,maxPosts=10000,includeOtherInfo=False,includeKeyBoard=False):
        self.User = User()
        self.User.twitterId = twitterId
        self.User.facebookId = facebookId

        self.maxTweets = maxTweets
        self.maxPosts = maxPosts
        self.customImagePath = customImagePath
        self.customStopWords = customStopWords
        self.bgColor = bgColor
        self.textColor = textColor
        self.includeOtherInfo = includeOtherInfo
        self.includeKeyBoard = includeKeyBoard

    def Visualize(self):
        print('getting statuses...')
        # get all statuses
        fbError = False
        if len(self.User.facebookId) > 0:
            try:
                self.User.statuses.extend(fh.getPosts(self.User))
            except:
                fbError = True
        liTweets = th.getTweets(self.User,maxTweets=self.maxTweets)
        if len(liTweets) == 0:
            return []
        self.User.statuses.extend(liTweets)
        
        # form string to cloud
        stringToCloud = ' '.join([x.statusText for x in self.User.statuses])
        stringToCloud = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9_]+)','',stringToCloud)

        # prepare custom stop words
        if self.customStopWords == None:
            self.customStopWords = list(STOPWORDS)

        self.customStopWords.append(self.User.twitterId.lower())
        for w in self.User.twitterName.split(' '):
            self.customStopWords.append(w.lower())
        self.customStopWords.append(self.User.twitterName.replace(' ','').lower())

        langs = [x.language for x in self.User.statuses]
        for lang in set(langs):
            if langs.count(lang) > 0.4 * len(self.User.statuses) and lang in global_stopwords:
                self.customStopWords.extend(global_stopwords[lang])

        print('getting profiles...')
        # get twitter profile for more information
        self.User = th.fetch_profile(self.User)

        kbImgPath = "outputImages\\" + self.User.twitterId + "_keyboard.png"
        keyBoardImage = createKeyBoardHeatMap(stringToCloud)
        keyBoardImage.save(kbImgPath)
        
        # prepare mask
        if self.customImagePath == None:
            self.customImage = Image.open(BytesIO(requests.get(self.User.twitterImageURL).content))
        else:
            self.customImage = Image.open(self.customImagePath)
        
        print('making pictues...')
        # make images
        liImages = Visualizer(self.User,stringToCloud,self.customImage,self.customStopWords,self.bgColor,self.textColor,keyBoardImage,self.includeOtherInfo,self.includeKeyBoard).Visualize()

        # cleanUp
        self.customImage.close()

        if self.User.twitterId.lower() in self.customStopWords:
            self.customStopWords.remove(self.User.twitterId.lower())
        for w in self.User.twitterName.lower().split(' '):
            if w in self.customStopWords:
                self.customStopWords.remove(w)
        if self.User.twitterName.replace(' ','').lower() in self.customStopWords:
            self.customStopWords.remove(self.User.twitterName.replace(' ','').lower())

        return liImages,kbImgPath,fbError

def initialize_global_stopwords(code,language):
    global global_stopwords
    global_stopwords[code] = []
    try:
        with open('stopwords-' + code + '.txt') as f:
            global_stopwords[code] = f.readlines()
        global_stopwords[code] = [x.strip() for x in global_stopwords[code]]
    except:
        pass
    if len(language) > 0:
        for word in stopwords.words(language):
            if word.lower() not in global_stopwords[code]:
                global_stopwords[code].append(word.lower())

def getImages(twitterId,facebookId='',customImagePath=None, bgColor="black",textColor="multi",maxTweets=10000,maxPosts=10000):
    global global_stopwords
    if len(global_stopwords) == 0:
        initialize_global_stopwords('en','english')
        initialize_global_stopwords('de','german')
        initialize_global_stopwords('es','spanish')
        initialize_global_stopwords('it','italian')
        initialize_global_stopwords('no','norwegian')
        initialize_global_stopwords('fr','french')
        initialize_global_stopwords('da','danish')
        initialize_global_stopwords('fi','finnish')
        initialize_global_stopwords('hu','hungarian')
        initialize_global_stopwords('pt','portuguese')
        initialize_global_stopwords('sv','swedish')
        initialize_global_stopwords('nl','dutch')
        initialize_global_stopwords('ru','russian')
        initialize_global_stopwords('tr','turkish')
        pass

    stpwrds = list(STOPWORDS)
    stpwrds.append('gt')
    stpwrds.append('rt')        
    return SocialVisualizer(twitterId,facebookId,customImagePath=customImagePath,customStopWords=stpwrds,bgColor=bgColor,textColor=textColor,maxTweets=maxTweets,maxPosts=maxPosts).Visualize()

#def main():
#    vis = SocialVisualizer("sptiwari97",maxTweets=100)
#    print(vis.Visualize())
#    #print(SocialVisualizer("WildguyzEDM",maxTweets=100).Visualize())
#if __name__ == "__main__":
#    main()