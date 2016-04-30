class Status:
    def __init__(self):
        self.statusText = ''
        self.statusType = -1
        self.CreatedOn = ''
        self.likes = -1
        self.shares = -1
        self.id = -1
        self.language = 'en'

    def __repr__(self, **kwargs):
        return str(self)

    def __str__(self):
        return ('Twitter:' if self.statusType == 1 else 'Facebook:') + self.statusText + ':' + str(self.likes) + ':' + str(self.shares)