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
#from search_user import SearchUser


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ProfilePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        following = 0
        following_list = []
        followers = 0
        followers_list = []
        user_following = False
        user_following_list = []


        user = users.get_current_user()
        username = self.request.get('user')
        getRandomUser = MyUser.get_by_id(username)
        x = Posts.query().filter(Posts.email == username).fetch()
        posts_key = ndb.Key('Posts', user.email())
        postsdbId = posts_key.get()
        user_key = ndb.Key('MyUser', user.email())
        user_info = user_key.get()
        getCurrentUser = MyUser.get_by_id(user.email())
        


        
        for x in getCurrentUser.following:
            user_following_list.append(x)


        if username in user_following_list:
            user_following = True


        for x in getRandomUser.following:
            following_list.append(x)


        for x in getRandomUser.followers:
            followers_list.append(x) 


        following = len(following_list)
        followers = len(followers_list)
        
        
        template_values = {
            'user': user,
            'current_user' : user.email(),
            'random_user' : username,
            'followers' : followers,
            'following' : following,
            'user_following' : user_following,
            'var_name' : x
        }


        template = JINJA_ENVIRONMENT.get_template('profile_page.html')
        self.response.write(template.render(template_values))
    

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        current_user = self.request.get('current_user')
        random_user = self.request.get('random_user')
        get_current_user = MyUser.get_by_id(current_user)
        get_random_user = MyUser.get_by_id(random_user)
        

        action = self.request.get('button')


        if action == 'follow_user':

            get_current_user.following.append(random_user)
            get_current_user.put()
            get_random_user.followers.append(current_user)
            get_random_user.put()

            self.redirect('/profile_page?user='+ current_user)
