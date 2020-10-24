import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import os


from myuser import MyUser
from posts import Posts
from create_post import CreatePost
from uploadhandler import UploadHandler
#from re import search
# from profile_page import ProfilePage


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'
        email = ''
        myuser = ''
        user = users.get_current_user()


        template_values = {
            'user' : user,
            'upload' : blobstore.create_upload_url('/upload')
        }


        template = JINJA_ENVIRONMENT.get_template('search_user.html')
        self.response.write(template.render(template_values))

    
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        search_username = self.request.get('search')
        print search_username

        if self.request.get('button') == 'search_user':
           search_result = MyUser.query().filter(MyUser.email == search_username).fetch()

        template_values = {
            'user' : user,
            'instagram' : search_result
        }

        template = JINJA_ENVIRONMENT.get_template('search_user.html')
        self.response.write(template.render(template_values))