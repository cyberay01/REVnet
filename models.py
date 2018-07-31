from google.appengine.ext import ndb

class Locations(ndb.Model):
    host_name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    comment = ndb.StringProperty(required=False)
    longitude = ndb.FloatProperty(required=False)
    latitude = ndb.FloatProperty(required=False)
    created_at = ndb.DateTimeProperty(required=False)

