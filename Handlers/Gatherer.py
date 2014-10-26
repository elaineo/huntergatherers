from Handlers.BaseHandler import *
import logging
import json
from Populate import *
from Models.Users import *
from data.globallinks import links

class Gatherer(BaseHandler):
    def get(self, action):
        if action=='f':
            self.__followers()
        elif action=='bb':
            self.__buttbuddies()
            
    def __buttbuddies(self):
        username = self.request.get('username')
        user = PHUser.by_username(username).get()
        if not user:
            self.write('User not found')
            return
        # only pick out ppl directly connected 
        linkfilter = []        
        for l in links:
            if int(l[0])==user.id or int(l[1])==user.id:
                linkfilter.append(l)
        nodes = []  
        for l in linkfilter:
            if int(l[0]) not in nodes:
                nodes.append(int(l[0]))
            if int(l[1]) not in nodes:
                nodes.append(int(l[1]))
        usernodes = [PHUser.by_id(n) for n in nodes]
        # filter links again
        linkfilter = []
        for l in links:
            if int(l[0]) in nodes and int(l[1]) in nodes:
                linkfilter.append(l)        
        nodedump = [{'name': nd.username, 'id': nd.id} for nd in usernodes]
        nodeindex = [n['id'] for n in nodedump]
        linkdump = sortlinks(nodeindex, linkfilter)
        self.write(json.dumps({'nodes':nodedump, 'links':linkdump}))
        
        
    def __followers(self):
        self.response.headers['Content-Type'] = "application/json"
        data = json.loads(self.request.body)
        username = data.get('username')
        user = PHUser.by_username(username).get()
        if not user:
            self.write('User not found')
            return
        nodes = []
        for f in user.followers + users.followees:
            if f not in nodes:
                nodes.append(f)
        # filter out links
        usernodes = [n.get() for n in nodes]
        nodes = [n.id for n in usernodes]
        linkfilter = []
        for l in links:
            if int(l[0]) in nodes or int(l[1]) in nodes:
                linkfilter.append(l)
        # links = linkfilter
        nodedump = [{'name': nd.username, 'id': nd.id} for nd in usernodes]
        nodeindex = [n.id for n in nodedump]
        linkdump = sortlinks(nodeindex, linkfilter)
        self.write(json.dumps({'nodes':nodedump, 'links':linkdump}))