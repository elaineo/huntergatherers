from Handlers.BaseHandler import *
import logging
import json
from Populate import *
from Models.Users import *
from data.everybody import everybody

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
            users,cursor,more = PHUser.query().order(-PHUser.id).fetch_page(1000)
            dump = {}
            count = 0            
            for u in users:
                dump[str(u.id)] = {'username': u.name}
            d = DumpObject(dump=dump, count=count).put()
            while more:
                dump = {}
                count = count+1
                users,cursor,more = PHUser.query().order(-PHUser.id).fetch_page(1000, start_cursor=cursor)
                for u in users:
                    dump[str(u.id)] = {'username': u.name}
                d = DumpObject(dump=dump, count=count).put()
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
        elif action=='viewusers':
            
        else:
            populate_follower(action)