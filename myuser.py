from google.appengine.ext import ndb
#from posts import Posts


class MyUser(ndb.Model):
    email = ndb.StringProperty()
    #username = ndb.StringProperty()
    #posts = ndb.StructuredProperty(Posts, repeated=True)
    followers = ndb.StringProperty(repeated=True)
    following = ndb.StringProperty(repeated=True)