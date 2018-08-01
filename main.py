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

#only page accessable by users that are not logged in
class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render({'login_url': users.create_login_url('/')}))


class MainPage(webapp2.RequestHandler):
    def get(self):
    #checking if the user is actually logged in
        template_var = {}
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            template_var = {
                "logout_url": logout_url,
                "nickname": nickname
            }
    #if the user is not logged in, redirect to welcome
        else:
            self.redirect('/welcome')
        main_template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(main_template.render(template_var))


class MapPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
    #check for user login
        if user:
            pass
    #fetch() - fetch the first 10 entries(from the database)
        else:
            self.redirect('/welcome')
        locations = Locations.query().fetch(10)
        map_template = JINJA_ENVIRONMENT.get_template('templates/map.html')
        self.response.write(map_template.render({'locations': locations}))

#show the uploaded locations after since
class UpdatedMapPage(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/json' #return text of json when accessed
        since = float(self.request.get('since'))#'since' is the query
        since_dt = datetime.datetime.fromtimestamp(since)
        new_locations = Locations.query(Locations.created_at >= since_dt).fetch()
        new_location_list = []
        #dictionary is converted to json
        for location in new_locations:
            new_location_list.append({
                'host_name': location.host_name,
                'address': location.address,
                'comment': location.comment,
            })
        self.response.write(json.dumps(new_location_list)) #converts to json and shows pure json file /map can cation locations as a list

class LocationPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template_var = {}
            user = users.get_current_user()
            if user:
                logout_url = users.create_logout_url('/')
                template_var = {
                    "logout_url": logout_url,
                    }
        else:
            self.redirect('/welcome')
        locations_template = JINJA_ENVIRONMENT.get_template('templates/locations.html') #post data and add locations(html)
        self.response.write(locations_template.render(template_var))

    def post(self):#upload as a datastore entries
        Locations(host_name=self.request.get('host_name'),
            address = self.request.get('address'),
            comment = self.request.get('comment'),
            created_at = datetime.datetime.now()).put()
        self.redirect('/map') #redirected to the map

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage),
    ('/map', MapPage),
    ('/locations', LocationPage),
    ('/updated_list', UpdatedMapPage)
], debug=True)
