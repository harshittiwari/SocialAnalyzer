import TwitterHelper as th
from SocialVisualizer import getImages
import ImgurHelper as ih
import time
import os
from dateutil.parser import parse
import datetime
import random
from User import User

createdBy = 'Created By: https://twitter.com/social_visualiz'

emoticons = [':‑)',':)',':D',':o)',':]',':3',':c)',':>','=]','8)','=)',':}',':^)',':っ)',':‑D','8‑D','8D','x‑D','xD','X‑D','XD','=‑D','=D','=‑3','=3','B^D',':-))',":'‑)",":')",';‑)',';)','*-)','*)',';‑]',';]',';D',';^)',':‑,',
             'O:‑)','0:‑3','0:3','0:‑)','0:)','0;^)','( ͡° ͜ʖ ͡°)','\o/','*\0/*','<3','^_^','(゜o゜)','(^_^)/','(^O^)／','(^o^)／','(^^)/','(≧∇≦)/','(/◕ヮ◕)/','(^o^)丿','∩(・ω・)∩','(・ω・)','^ω^','＼(~o~)／','＼(^o^)／','＼(-o-)／','ヽ(^。^)ノ','ヽ(^o^)丿','(*^0^*)',
             '(*^^)v','(^^)v','(^_^)v','(＾▽＾)','（・∀・）','（　´∀｀）','（⌒▽⌒）','（＾ｖ＾）','（’-’*)','（●＾o＾●）','（＾ｖ＾）','（＾ｕ＾）','（＾◇＾）','(','^)o(^',')','(^O^)','(^o^)','(^○^)',')^o^(','(*^▽^*)','(✿◠‿◠)',
             '( ﾟヮﾟ)','キタ━━━(゜∀゜)━━━!!!!! ','⊂二二二（　＾ω＾）二⊃','( ﾟдﾟ)','(・o･)']

def addEmoticons(s):
    i = 0
    while len(s) < 135 and i < 1:
        rand_emoticon = random.choice(emoticons)
        if len(rand_emoticon) + len(s) < 137:
            i += 1
            s += '  ' + rand_emoticon
    return s

def getUsers():
    li = []
    with open('usersDone.txt') as f:
        li = f.readlines()
    dict = {}
    for el in li:
        user,url,kurl = el.strip().split(' ')
        dict[user.lower()] = [url,kurl]
    return dict

def getLastRead():
    d = None
    with open('lastRead.txt') as f:
        d = f.read()
    return parse(d)

def getSelfRequest(text):
    text = text.strip()
    li = text.split(' ')
    if len(li) == 2:
        return {}
    else:
        li2 = {}
        if li[2].startswith('@'):
            li2['target'] = li[2][1:]
        for el in li:
            if el.startswith('bg='):
                li2['bg'] = el.split('=')[1]
            elif el.startswith('tc='):
                li2['tc'] = el.split('=')[1]
            elif el.startswith('fb='):
                li2['fb'] = el.split('=')[1]
        return li2

def SearchCustomRequest(usersDone):
    li = []
    with open('customRequest.txt') as f:
        li = f.readlines()
    random.shuffle(li)
    for el in li:
        d = getSelfRequest(el.strip())
        target = d['target']
        bgColor = 'black'
        textColor = 'multi'
        fb = ''
        if 'bg' in d:
            bgColor = d['bg']
        if 'tc' in d:
            textColor = d['tc']
        if 'fb' in d:
            fb = d['fb']
        if target.lower() not in usersDone:
            return True,target,target,bgColor,textColor,fb
    return False,'','','black','multi',''

def tweetResponse(request,target,albumId,keyBoardHeatMapId,isOld=False,fbError=False):
    #isPosted = False
    #while not isPosted:
    if albumId == '-' or keyBoardHeatMapId == '-':
        th.postUpdate('Hi @' + request + " there was an error while processing your request. We'll be looking into this, plz msg if its urgent")
    else:
        s = None
        if request != target:
            s = 'hey @' + request + ', for customized #wordcloud album for @' + target + ' go to http://imgur.com/a/' + albumId
        else:
            s = 'hey @' + request + ', for your customized #wordcloud album go to http://imgur.com/a/' + albumId 
        #if len(s) < 135:

        y = th.postUpdate(addEmoticons(s))
        print(s)
        #time.sleep(60)
        if request != target:
            s = 'hey @' + request + ', to see #keyboardheatmap for @' + target + ' go to http://imgur.com/' + keyBoardHeatMapId
        else:
            s = 'hey @' + request + ', to see your #keyboardheatmap go to http://imgur.com/' + keyBoardHeatMapId
        x = th.postUpdate(addEmoticons(s))
        print(s)
    if isOld:
        s = 'Hey @' + request + ', request for @' + target + ' was processed earlier & old result was returned. If u need new results, message me'
        th.postUpdate(s)
        print(s)
    if fbError:
        s = 'Hey @' + request + ', your request was only processed on twitter profile as your facebook page is not public. For details, message me.'
        th.postUpdate(s)
        print(s)

pendingUsers = []
def SearchMention(term, usersDone,lastread):
    global pendingUsers 
    isFound = False
    target = ''
    request = ''
    bgColor = 'black'
    textColor = 'multi'
    fb = ''
    if len(pendingUsers) == 0:
        obj = th.getMentions(term)
        while len(obj['statuses']) > 0:
            for status in obj['statuses']:
                if not status['text'].startswith(term):
                    continue
                if not status['favorited']:
                    th.favouriteTweet(status['id'])
                curdt = parse(status['created_at'])
                if  curdt <= lastread:
                    isFound = True
                    break
                d = getSelfRequest(status['text'])
                if 'target' not in d:
                    target = status['user']['screen_name']
                else:
                    target = d['target']
                if 'bg' in d:
                    bgColor = d['bg']
                if 'tc' in d:
                    textColor = d['tc']
                if 'fb' in d:
                    fb = d['fb']
                request = status['user']['screen_name']
                pendingUsers.append([True,target,request,bgColor,textColor,fb,curdt])
                target = ''
                request = ''
                bgColor = 'black'
                textColor = 'multi'
                fb = ''
            if isFound:
                break
            obj = th.getMentions(term,obj['search_metadata']['max_id_str'])

    if len(pendingUsers) > 0:
        return pendingUsers.pop()
    else:
        return False,target,request,bgColor,textColor,fb,None

def updateLastRead(curDt):
    with open("lastRead.txt", "w") as myfile:
        myfile.write(str(curDt))

def getWhoIFollow():
    prev_followers = []
    with open('WhoIFollow.txt') as f:
        prev_followers = f.readlines()
    return set([x.strip().lower() for x in prev_followers])

def main():
    following = list(getWhoIFollow())
    usersDone = getUsers()
    lastread = getLastRead()
    switch = False
    while True:
        #while True:
        #    rtTweets = th.getTweets(User(random.choice(following)),True,False,10,False)
        #    rtTweets = [x for x in rtTweets if (datetime.datetime.now - parse(x.CreatedOn)) < 2]
        #    if len(rtTweets) > 0:
        #        x = th.reTweet(random.choice(rtTweets).id)
        #        break
        isFound = False
        target = ''
        request = ''
        bgColor = 'black'
        textColor = 'multi'
        fb = ''

        term = '@social_visualiz #wordcloud'
        curDt = None
        isFound,target,request,bgColor,textColor,fb,curDt = SearchMention(term, usersDone,lastread)
        
        #if not isFound and switch:
        #    isFound,target,request,bgColor,textColor,fb =
        #    SearchCustomRequest(usersDone)

        #if not isFound:
        #    term = '@wordnuvola #wordcloud'
        #    isFound,target,request,bgColor,textColor,fb =
        #    SearchMention(term,usersDone)
            
        if not isFound:
            isFound,target,request,bgColor,textColor,fb = SearchCustomRequest(usersDone)

        switch = not switch
        if isFound:
            albumId = '-'
            keyBoardHeatMapId = '-'
            count = 0
            if target.lower() not in usersDone:
                fbError = False
                while count < 3:
                    try:
                        print(target + '...')
                        liImages,kbImgPath,fbError = getImages(target,fb,bgColor=bgColor,textColor=textColor)
                        ids = []
                        print('uploading pictures...')
                        for img in liImages:
                            imgName = img.split('\\')[1]
                            s = imgName.split('_')[0]
                            ids.append(ih.UploadPhoto(img,s,s,'Wordcloud for ' + target)['id'])
                            os.remove(img)
                            os.remove('rawImages\\' + imgName)
                        albumId = ih.CreateAlbumAndUploadImages('Portrait WordCloud For @' + target,'Portrait WordCloud For @' + target + ' ' + createdBy,ids)['id']
                        kbImgName = kbImgPath.split('\\')[1]
                        s = kbImgName.split('_')[0]
                        keyBoardHeatMapId = ih.UploadPhoto(kbImgPath,s,s,'KeyBoard Heatmap for ' + target)['id']
                        os.remove(kbImgPath)
                        ih.UploadPhotoInAlbum(keyBoardHeatMapId,'nYqIT')
                        break
                    except:
                        count += 1
                        time.sleep(960)
                if albumId == '-' or keyBoardHeatMapId == '-':
                    with open("errorUser.txt", "a") as myfile:
                        myfile.write(target + '\n')
                usersDone[target.lower()] = [albumId,keyBoardHeatMapId]
                print('tweeting...')
                tweetResponse(request,target,albumId,keyBoardHeatMapId,fbError=fbError)
                with open("usersDone.txt", "a") as myfile:
                    myfile.write(target + ' ' + albumId + ' ' + keyBoardHeatMapId + '\n')
            else:
                tweetResponse(request,target,usersDone[target.lower()][0],usersDone[target.lower()][1],True)
            if curDt is not None:
                updateLastRead(curDt)
                lastread = curDt
        print('sleeping...')
        time.sleep(600)
        #for i in range(3):
        #    rtTweets = th.getTweets(User(random.choice(following)),True,False,10,False)
        #    x = th.reTweet(random.choice(rtTweets).id)
        #    time.sleep(500)
    pass

if __name__ == '__main__':
    main()



# https://github.com/SMAPPNYU/smappPy/tree/master/smappPy
# https://github.com/robrant/wordslang/tree/master/baseData