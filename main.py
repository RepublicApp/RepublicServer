from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):
        for i in range(30):
            self.response.out.write('Hello world!\n')

app = webapp.WSGIApplication([('/', MainHandler)],
                             debug=True)

