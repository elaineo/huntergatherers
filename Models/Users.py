from google.appengine.ext import ndb

class PHUser(ndb.Model):
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    headline = ndb.StringProperty()
    id = ndb.IntegerProperty()
    followers = ndb.KeyProperty(repeated=True)
    following = ndb.KeyProperty(repeated=True)

    @classmethod
    def by_id(cls, id):
        c = cls.query(cls.id == id).get_async()
        return c
    
    @classmethod
    def key_by_id(cls, id):
        c = cls.query(cls.id == id).get(keys_only=True)
        return c

    @classmethod
    def newest(cls):
        c = cls.query().order(-cls.id).get()
        return c

    @classmethod
    def oldest(cls):
        c = cls.query().order(cls.id).get()
        return c
        
    @classmethod
    def by_username(cls, name):
        c = cls.query(cls.username == name)
        return c
        
    @classmethod
    def by_name(cls, name):
        c = cls.query(cls.name == name)
        return c
        
class DumpObject(ndb.Model):
    dump = ndb.JsonProperty()
    count = ndb.IntegerProperty()