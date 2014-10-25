from Handlers.BaseHandler import *
import logging
import json

class HomePage(BaseHandler):
    """ Home page, first page shown """
    def get(self):
        self.render('home.html', **self.params)
