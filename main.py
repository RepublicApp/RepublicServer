import webapp2
from google.appengine.ext import db

class Image(db.Model):
    uploader    = db.StringProperty()
    description = db.StringProperty(multiline=True)
    image       = db.BlobProperty()
    date        = db.DateTimeProperty(auto_now_add=True)

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        img = db.get(self.request.get('id'))
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(img.image)

    def post(self):
        img = Image()
        img.uploader = self.request.get('uploader')
        img.description = self.request.get('description')
        img.image = db.Blob(self.request.get('image'))
        img.put()
        self.response.out.write('Uploaded')

class TestUploader(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
        <html>
            <body>
                <form action="/image?%s" enctype="multipart/form-data" method="post">
                    <div><input type="file" name="image"/></div>
                    <div><input type="submit" value="Upload!"></div>
                </form>
            </body>
        </html>""")

class MainHandler(webapp2.RequestHandler):
    robot_img = "http://cdn4.iconfinder.com/data/icons/REALVISTA/mobile/png/128/android_platform.png"

    def get(self):
        self.response.out.write('<html>\n<body>\n')
        self.response.out.write('<div style="width:100%;">\n')

        images = Image.gql('')      # Get all Image objects from the data store
        for image in images:
            self.response.out.write('<img src="image?id=%s"/>' % image.key())
        self.response.out.write('</div>\n')
        self.response.out.write('</body>\n</html>')

app = webapp2.WSGIApplication([ ('/', MainHandler),
                                ('/image', ImageHandler),
                                ('/uploader', TestUploader)],
                                debug = True)

