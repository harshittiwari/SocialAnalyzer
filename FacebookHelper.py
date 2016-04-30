from FacebookAPI import GraphAPI
from Status import Status
import re
import Config

at = Config.fb_access_token

def validPost(text):
    t = re.sub('@[^\s]+','',text,flags=re.MULTILINE)
    t = re.sub('[^a-zA-Z]','',t)
    if len(t) > 5:
        return True
    return False

def getPosts(user,clean=True,maxPosts=100):
    try:
        userName = user.facebookId
        args = {}

        graph = GraphAPI(at)
        profile = graph.get_object(userName)
        posts = graph.get_connections(profile['id'], 'posts', **args)
        statuses = []
        lastUntil = ''
    
        for s in posts['paging']['next'].split('&'):
            if 'limit=' in s:
                args['limit'] = s.split('=')[1]
            if 'until=' in s:
                args['until'] = s.split('=')[1]
        while True:
            isBreak = False
            for data in posts['data']:
                if 'message' not in data:
                    continue
                smessage = str(data['message'].encode("utf-8")).replace('\\n', ' ').replace('\\r', '')[2:-1]
                if clean:
                    smessage = re.sub(r'https?:\/\/[^\s]*','',smessage, flags=re.MULTILINE)
                    smessage = re.sub(r'\\x..','',smessage, flags=re.MULTILINE)
                    smessage = re.sub(r'&amp;','and',smessage, flags=re.IGNORECASE)
                    smessage = re.sub(r'[\s\t]+',' ',smessage, flags=re.IGNORECASE)
                    smessage.replace('#','')

                if validPost(smessage):
                    st = Status()
                    st.statusText = smessage
                    st.id = data['id']
                    statuses.append(st)

            if len(statuses) > maxPosts:
                break
            posts = graph.get_connections(profile['id'], 'posts',**args)
            nargs = {}
            for s in posts['paging']['next'].split('&'):
                if 'limit=' in s:
                    nargs['limit'] = s.split('=')[1]
                if 'until=' in s:
                    nargs['until'] = s.split('=')[1]
            if nargs['until'] == args['until']:
                break
            else:
                args['limit'] = nargs['limit']
                args['until'] = nargs['until']
        return statuses
    except ConnectionError:
        return []