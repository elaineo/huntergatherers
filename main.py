import webapp2
import sys
from HomePage import *


app = webapp2.WSGIApplication([('/', HomePage)
],  debug=True)

