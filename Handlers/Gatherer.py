from Handlers.BaseHandler import *
import logging
import json
from Populate import *
from Models.Users import *
from data.globallinks import globallinks
from data.links import littlelinks
from data.people import people
import time
from google.appengine.api import memcache

class Gatherer(BaseHandler):
    def get(self, action):
        if action=='f':
            self.__followers()
        elif action=='bb':
            username = self.request.get('username')
            nodes = memcache.get(username)
            if not nodes:            
                nodes = self.__buttbuddies(username)
                memcache.add(key=username, value=nodes)
            self.write(nodes)

    def __buttbuddies(self, username):        
        user = PHUser.by_username(username).get()
        if not user:
            self.write('User not found')
            return
        center = {'name':username, 'id':user.id}
        links = littlelinks
        # only pick out ppl directly connected
        linkfilter = []
        for l in links:
            if int(l[0])==user.id or int(l[1])==user.id:
                linkfilter.append(l)
                
        if len(linkfilter) < 5:
            links = globallinks
            for l in links:
                if int(l[0])==user.id or int(l[1])==user.id:
                    linkfilter.append(l)
        nodes = []
        for l in linkfilter:
            if int(l[0]) not in nodes:
                nodes.append(int(l[0]))
            if int(l[1]) not in nodes:
                nodes.append(int(l[1]))
        logging.info(time.time())
        # filter links again
        if len(nodes) > 1000:
            links = littlelinks        
        linkfilter = []
        for l in links:
            if int(l[0]) in nodes and int(l[1]) in nodes:
                linkfilter.append(l)
        logging.info(time.time())
        nodedump = []
        for n in nodes:
            p = people.get(n)
            nodedump.append({'name': p, 'id': n})
        logging.info(time.time())
        nodeindex = [n['id'] for n in nodedump]
        centerindex = nodeindex.index(center['id'])
        logging.info(centerindex)
        linkdump = sortlinks(nodeindex, linkfilter)
        return json.dumps({'nodes':nodedump, 'links':linkdump, 'center':center, 'centerindex': centerindex})


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
