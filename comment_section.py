from google.appengine.ext import ndb


class CommentSection(ndb.Model):
    email = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    user_comment = ndb.StringProperty()