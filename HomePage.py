from Handlers.BaseHandler import *
from Models.Users import *
import logging
from google.appengine.api import taskqueue

class HomePage(BaseHandler):
    """ Home page, first page shown """
    def get(self):
        taskqueue.add(url='/actions/dumpusers', method='get')
        self.render('home.html', **self.params)

class TestPage(BaseHandler):
    def get(self):
        """ dump list of user ids and respective followers, followees
          {'name': x, 'id': x, 'followers': x, 'followees': x} 
        """
        users = PHUser.query()
        dump = []
        for u in users:
            d = {'name': u.username, 'id': u.id}
            if len(u.followers)>0:
                d['followers'] = [f.get().id for f in u.followers]
            if len(u.following)>0:
                d['following'] = [f.get().id for f in u.following]
            dump.append(d)
        self.write(dump)