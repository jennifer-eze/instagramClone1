import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


from myuser import MyUser
from posts import Posts
from uploadhandler import UploadHandler


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MyFollowersList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        userName = self.request.get('user')
        getAllUsers = MyUser.get_by_id(userName)
        user = users.get_current_user()


        template_values = {
            'followers' : getAllUsers.followers,
            'user' : user
        }


        template = JINJA_ENVIRONMENT.get_template('my_followers_list.html')
        self.response.write(template.render(template_values))