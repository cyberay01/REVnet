from google.appengine.ext import ndb #class provided by google app engine

#data you want to be stored in datastore
# only way for info to be seen by user
class Locations(ndb.Model):
    host_name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    comment = ndb.StringProperty(required=False)
    created_at = ndb.DateTimeProperty(required=False)
