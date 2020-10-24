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
from profile_page import ProfilePage
from search_user import SearchUser
from my_following_list import MyFollowingList
from my_followers_list import MyFollowersList
from comment_section import CommentSection


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        url = ''
        url_string = ''
        welcome = 'Welcome back to Instagram'
        user_timeline = ''
        user_timeline_list = []


        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            email = user.email()


            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()


            user_timeline = Posts.query().fetch()
            for signedin_user in user_timeline:
                if(signedin_user.email == user.email()):
                    user_timeline_list.append(signedin_user)


            if hasattr(myuser, 'following'):
                for person in myuser.following:
                    for data in user_timeline:
                        if(data.email == person):
                            user_timeline_list.append(data)
                    

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.email())
                myuser.email = user.email()
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
    

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'user_timeline_list' : user_timeline_list,
            'user_timeline' : user_timeline
        }


        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back to Instagram'
        user_timeline = ''
        user_timeline_list = []

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()
        comments = self.request.get('comment')
        postid = self.request.get('id')

        user_timeline = Posts.query().fetch()
        for signedin_user in user_timeline:
            if(signedin_user.email == user.email()):
                user_timeline_list.append(signedin_user)

        
        if hasattr(myuser, 'following'):
            for person in myuser.following:
                for data in user_timeline:
                    if(data.email == person):
                        user_timeline_list.append(data)


        if self.request.get('button') == 'add_comment':
            get_Post = Posts.get_by_id(int(postid))
            NewComment = CommentSection(email= user.email(), user_comment = comments)
            get_Post.user_comment.append(NewComment)
            get_Post.put()

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'user_timeline_list' : user_timeline_list,
            'user_timeline' : user_timeline
        }


        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create_post', CreatePost),
    ('/upload', UploadHandler),
    ('/profile_page', ProfilePage),
    ('/search_user', SearchUser),
    ('/follow_list', MyFollowingList),
    ('/followers_list', MyFollowersList),
], debug=True)