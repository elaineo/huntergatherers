import json
import requests
from Models.User import *

def populate_users():
    r = requests.get('https://api.producthunt.com/v1/users', headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
    dump = json.loads(r.content)
    for d in dump['users']:
        id = int(d.get('id'))
        ph = PHUser.by_id(id)
        if ph:
            continue
        ph = PHUser(username = d.get('username'), name = d.get('name'), headline = d.get('headline'), id = id, followers=[], following=[])
        ph.put()
        
def populate_followers():
    users = PHUser.query()
    for u in users:
        f_url = 'https://api.producthunt.com/v1/users/1/followers?userid=%s' % u.username
        r = requests.get(f_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
        dump = json.loads(r.content)
        
        for d in dump['followers']:
            f = PHUser.key_by_id(int(d.get('id')))
            u.followers.append(f)
        u.put()
        
        f_url = 'https://api.producthunt.com/v1/users/1/following?userid=%s' % u.username
        r = requests.get(f_url, headers={'Authorization': 'Bearer 2fa5f88e60dc5f7c90f076bd17eb65e9cc4608490d0e5ba2f316e05acd14794a'})
        dump = json.loads(r.content)
        
        for d in dump['following']:
            f = PHUser.key_by_id(int(d.get('id')))
            u.following.append(f)
        u.put()