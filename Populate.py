import logging
import json
import requests
from Models.Users import *
from data.links import littlelinks
from data.nodes import nodes
from data.everybody import everybody

def nodes_to_dict():
    nodedump = []
    nodeindex = []
    for n in nodes:
        nodedump.append({'name': n[1]})
        nodeindex.append(n[0])
    return nodedump, nodeindex
    
def links_to_dict():
    linkdump = []
    nodedump, nodeindex = nodes_to_dict()
    for l in links:
        source = nodeindex.index(int(l[0]))
        target = nodeindex.index(int(l[1]))
        linkdump.append({'source': source, 'target': target, 
            'value': int(l[2])})
    return linkdump, nodedump
    
def sortlinks(nodes, links):
    linkdump = []
    for l in links:
        source = nodes.index(int(l[0]))
        target = nodes.index(int(l[1]))
        linkdump.append({'source': source, 'target': target, 
            'value': int(l[2])})
    return linkdump
    
def populate_users():    
    x = 100000
    while x > 0:
        u_url = 'https://api.producthunt.com/v1/users?older=%s' % str(x)
        r = requests.get(u_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
        dump = json.loads(r.content)    
        for d in dump['users']:
            id = int(d.get('id'))
            ph = PHUser.by_id(id)
            if ph.get():
                continue
            ph = PHUser(username = d.get('username'), name = d.get('name'), headline = d.get('headline'), id = id, followers=[], following=[])
            ph.put()
        
        oldperson = PHUser.oldest()
        x = oldperson.id
        logging.info(x)
        
def populate_followers():
    users = PHUser.query()
    for u in users:
        f_url = 'https://api.producthunt.com/v1/users/1/followers?userid=%s' % u.username
        r = requests.get(f_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
        dump = json.loads(r.content)   
        
        if not u.followers:
            u.followers = []
        for d in dump['followers']:
            fuser = d.get('user')
            f = PHUser.key_by_id(int(fuser.get('id')))
            if not f:
                continue
            if f in u.followers:
                continue
            u.followers.append(f)
        
        f_url = 'https://api.producthunt.com/v1/users/1/following?userid=%s' % u.username
        r = requests.get(f_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
        dump = json.loads(r.content)
        
        for d in dump['following']:
            fuser = d.get('user')
            f = PHUser.key_by_id(int(fuser.get('id')))
            if not f:
                continue
            if f in u.followers:
                continue
            u.following.append(f)
        u.put()
        
def populate_follower(username):
    u = PHUser.by_username(username).get()
    f_url = 'https://api.producthunt.com/v1/users/1/followers?userid=%s' % u.username
    r = requests.get(f_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
    dump = json.loads(r.content)   
    
    if not u.followers:
        u.followers = []
    for d in dump['followers']:
        fuser = d.get('user')
        f = PHUser.key_by_id(int(fuser.get('id')))
        if not f:
            continue
        if f in u.followers:
            continue
        u.followers.append(f)
    
    f_url = 'https://api.producthunt.com/v1/users/1/following?userid=%s' % u.username
    r = requests.get(f_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
    dump = json.loads(r.content)
    
    for d in dump['following']:
        fuser = d.get('user')
        f = PHUser.key_by_id(int(fuser.get('id')))
        if not f:
            continue
        if f in u.followers:
            continue
        u.following.append(f)
    u.put()