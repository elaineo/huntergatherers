from Handlers.BaseHandler import *
import logging
import json
from Populate import *
from Models.Users import *
from data.everybody import everybody
from data.people import people

class ActionHandler(BaseHandler):
    def get(self, action):
        if action=='users':            
            populate_users()
        elif action=='followers':            
            populate_followers()
        elif action=='json':
            links, nodes = links_to_dict()
            #nodes = nodes_to_dict()
            self.write(json.dumps(everybody))
        elif action=='dumpusers':
            self.write(people)
        elif action=='dumpff':
            users = PHUser.query()
            dump = {}
            for u in users:
                d = {'name': u.username, 'id': u.id}
                if len(u.followers)>0:
                    d['followers'] = [f.get().id for f in u.followers]
                if len(u.following)>0:
                    d['following'] = [f.get().id for f in u.following]
                dump.append(d)
            d = DumpObject(dump = dump).put()
        else:
            populate_follower(action)