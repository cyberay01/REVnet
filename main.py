import webapp2
from google.appengine.api import users
import jinja2
import os
from models import Locations

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render({'login_url': users.create_login_url('/')}))


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_var = {}
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            template_var = {
                "logout_url": logout_url,
                "nickname": nickname
            }
        else:
            self.redirect('/welcome')
        main_template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(main_template.render(template_var))

class MapPage(webapp2.RequestHandler):
    def get(self):
        locations = Locations.query().fetch()
        for location in locations:
            self.response.write(location.host_name)
            self.response.write(location.street_name1)
            self.response.write(location.street_name2)
            self.response.write(location.comment)
            self.response.write("\n")
        #map_template = JINJA_ENVIRONMENT.get_template('templates/map.html')
        #self.response.write(map_template.render())

class LocationPage(webapp2.RequestHandler):
    def get(self):
        locations_template = JINJA_ENVIRONMENT.get_template('templates/locations.html')
        self.response.write(locations_template.render())

    def post(self):
        Locations(host_name=self.request.get('host_name'),
            street_name1 = self.request.get('street_name1'),
            street_name2 = self.request.get('street_name2'),
            comment = self.request.get('comment')).put()
        self.redirect('/map')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage),
    ('/map', MapPage),
    ('/locations', LocationPage),
], debug=True)
