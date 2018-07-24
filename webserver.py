from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi


def OpenIndexPage(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    restaurant_list = _session.query(Restaurant).all()

    list_in_html = ''
    for restaurant in restaurant_list:
        list_in_html += '''
            <p>
                {}</br>
                <a href='#'>Edit</a></br>
                <a href='#'>Delete</a>
            </p>
            '''.format(restaurant.name)

    output = '''
        <html>
        <body>
            <a href='/restaurants/new'>Make A New Restaurant Here</a>
            {}
        </body>
        </html>
        '''.format(list_in_html)

    self.wfile.write(output)
    print(output)
    return


def OpenCreatePage(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    output = '''
        <html>
        <body>
            <h1>Make A New Restaurant</h1>
            <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <input name='new_restaurant' type='text' placeholder="New Restaurant Name">
                <input type='submit' value='Create'>
            </form>
        </body>
        </html>
        '''

    self.wfile.write(output)
    print(output)
    return


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                OpenIndexPage(self)
                return

            if self.path.endswith("/restaurants/new"):
                OpenCreatePage(self)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = '''
                    <html>
                    <body>
                        <h2> Okay, how about this: </h2>
                        <h1> %s </h1>
                        <form method='POST' enctype='multipart/form-data' action='/hello'>
                            <h2>What would you like me to say?</h2>
                            <input name = 'message' type='text'>
                            <input type='submit' value='Submit'>
                        </form>
                    </body>
                    </html>
                    ''' % messagecontent[0]

            self.wfile.write(output)
            print(output)

        except:
            pass


def main():
    global _session

    try:
        engine = create_engine('sqlite:///restaurantMenu.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind = engine)
        _session = DBSession()

        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()