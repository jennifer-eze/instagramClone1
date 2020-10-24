from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.api.images import get_serving_url
from posts import Posts


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        text_caption = self.request.get('text_caption')
        print(text_caption)
        user = users.get_current_user()
        print(user.email())
        

        blobinfo = blobstore.BlobInfo(upload.key())
        filename = blobinfo.filename


        posts = Posts()
        image = get_serving_url(upload.key())
        print(image)


        posts.postname = filename
        posts.text_caption = text_caption
        posts.blobs = upload.key()
        posts.email = user.email()
        posts.image = image
        posts.put()


        self.redirect('/create_post')