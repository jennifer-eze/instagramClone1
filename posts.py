from google.appengine.ext import ndb
from comment_section import CommentSection


class Posts(ndb.Model):
    email = ndb.StringProperty()
    postname = ndb.StringProperty()
    text_caption = ndb.StringProperty()
    image = ndb.StringProperty()
    blobs = ndb.BlobKeyProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    user_comment = ndb.StructuredProperty(CommentSection, repeated=True)