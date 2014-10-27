import webapp2
import sys
from HomePage import *
from Handlers.ActionHandler import *
from Handlers.Gatherer import *


app = webapp2.WSGIApplication([('/', HomePage), 
    webapp2.Route('/about', handler=InfoPage),
    webapp2.Route('/gather/<action>', handler=Gatherer),
    webapp2.Route('/actions/<action>', handler=ActionHandler)
                               ],  debug=True)
