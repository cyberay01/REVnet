import webapp2
from google.appengine.api import users
import jinja2
import os
from models import Locations
import urllib
import datetime
import json

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
        locations = Locations.query().fetch(10)
        map_template = JINJA_ENVIRONMENT.get_template('templates/map.html')
        self.response.write(map_template.render({'locations': locations}))

class UpdatedMapPage(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/json'
        since = float(self.request.get('since'))
        since_dt = datetime.datetime.fromtimestamp(since)
        new_map = Locations.query(Locations.created_at >= since_dt).fetch()
        new_map_list = []
        for location in new_map:
            new_map_list.append({
                'host_name': location.host_name,
                'address': location.address,
                'comment': location.comment,
            })
        self.response.write(json.dumps(new_map_list))

class LocationPage(webapp2.RequestHandler):
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
        locations_template = JINJA_ENVIRONMENT.get_template('templates/locations.html')
        self.response.write(locations_template.render())

    def post(self):
        Locations(host_name=self.request.get('host_name'),
            address = self.request.get('address'),
            comment = self.request.get('comment'),
            created_at = datetime.datetime.now()).put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage),
    ('/map', MapPage),
    ('/locations', LocationPage),
    ('/updated_list', UpdatedMapPage),
], debug=True)
