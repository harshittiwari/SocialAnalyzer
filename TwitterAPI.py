# -*- coding: utf-8 -*-

import argparse
import oauth2 as oauth
import urllib.request as urllib
import urllib.error as urlliberr
import json
import sys
import csv
import re

class TwitterAPI:
    def __init__(self, access_token_key ,access_token_secret, consumer_key, consumer_secret,_debug=0):
        self.access_token_key = access_token_key 
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_secret
        self.consumer_secret = consumer_secret

        self._debug = 0

        self.oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
        self.oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

        self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

        self.http_handler = urllib.HTTPHandler(debuglevel=_debug)
        self.https_handler = urllib.HTTPSHandler(debuglevel=_debug)

    '''
    Construct, sign, and open a twitter request
    using the hard-coded credentials above.
    '''
    def twitterreq(self, url, parameters,method="GET"):
        req = oauth.Request.from_consumer_and_token(self.oauth_consumer,
                                                 token=self.oauth_token,
                                                 http_method=method,
                                                 http_url=url, 
                                                 parameters=parameters)

        req.sign_request(self.signature_method_hmac_sha1, self.oauth_consumer, self.oauth_token)

        headers = req.to_header()

        if method == "POST":
            encoded_post_data = req.to_postdata()
            encoded_post_data = encoded_post_data.encode('utf-8')
        else:
            encoded_post_data = None
            url = req.to_url()

        opener = urllib.OpenerDirector()
        opener.add_handler(self.http_handler)
        opener.add_handler(self.https_handler)
        response = None
        i = 0
        while response is None and i < 10:
            try:
                i += 1
                response = opener.open(url, encoded_post_data)
            except urlliberr.URLError:
                pass
        if response != None:
            response = opener.open(url, encoded_post_data)
        return response

    def fetch_by_terms(self, term,since=''):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        parameters = [("q", term)]
        if len(since) > 0:
            parameters.append(('since_id',since))
        response = self.twitterreq(url, parameters,"GET")
        return json.loads(response.readline().decode('utf-8'))

    def fetch_user_profile(self, name):
        url = "https://api.twitter.com/1.1/users/show.json"
        parameters = [("screen_name", name)]
        response = self.twitterreq(url, parameters,"GET")
        return json.loads(response.readline().decode('utf-8'))

    def post_update(self, status, media=None):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        parameters = [("status", status)]
        if media is not None:
            parameters.append(("media[]",media))
        response = self.twitterreq(url, parameters,"POST")
        return json.loads(response.readline().decode('utf-8'))

    def reTweet_post(self,postId):
        #url = "https://api.twitter.com/1.1/statuses/retweet/:id.json"
        url = "https://api.twitter.com/1.1/statuses/retweet/"+str(postId)+".json"
        parameters = [("id", postId)]
        response = self.twitterreq(url, parameters,"POST")
        return json.loads(response.readline().decode('utf-8'))


    def favourite_post(self,postId):
        url = "https://api.twitter.com/1.1/favorites/create.json"
        parameters = [("id", postId)]
        response = self.twitterreq(url, parameters,"POST")
        return json.loads(response.readline().decode('utf-8'))

    def fetch_followers_list(self,user_screenname, cursor=-1, count=200):
        url = "https://api.twitter.com/1.1/friends/list.json"
        parameters = [("screen_name", user_screenname.strip()),
                      ("cursor",cursor),
                      ("count",count)]
        response = self.twitterreq(url, parameters, "GET")
        for el in response:
            if response.status in [401,88]:
                continue
            followers = json.loads(el.decode("utf-8"))
            return followers

    def fetch_by_user_names(self, name,id=-1,clean=False, includeRetweets=False):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        parameters = [("screen_name", name.strip()),("count",200)]
        if id > 0:
            parameters.append(('max_id',id))
        response = self.twitterreq(url, parameters, "GET")
        liTweets = []
        for el in response:
            if response.status in [401,88]:
                continue
            tweets = json.loads(el.decode("utf-8"))
            return tweets