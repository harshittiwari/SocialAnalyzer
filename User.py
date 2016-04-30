class User:
    def __init__(self,twitterId=''):
        self.userid = -1
        self.username = ''

        self.twitterId = twitterId
        self.twitterFollower = -1
        self.twitterName = ''
        self.twitterImageURL = ''

        self.facebookId = ''

        self.statuses = []

    def __str__(self):
        return str(self.userid) + ':' + self.username + ':' + self.twitterId + ':' + self.facebookId