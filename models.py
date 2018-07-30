from google.appengine.ext import ndb

class Locations(ndb.Model):
    host_name = ndb.StringProperty(required=False)
    street_name1 = ndb.StringProperty(required=False)
    street_name2 = ndb.StringProperty(required=False)
    comment = ndb.StringProperty(required=False)
    #longitude = ndb.FloatProperty(required=True)
    #latitude = ndb.FloatProperty(required=True)

