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
                <a href='/restaurants/{}/edit'>Edit</a></br>
                <a href='/restaurants/{}/delete'>Delete</a>
            </p>
            '''.format(restaurant.name, str(restaurant.id), str(restaurant.id))

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


def OpenEditPage(self):
    #Get the restaurant id from the path
    path_elements = self.path.split('/')
    id_string = path_elements[len(path_elements) - 2]
    restaurant_id = int(id_string)

    #Find restaurant to edit
    restaurant = _session.query(Restaurant).filter_by(id = restaurant_id).first()

    if restaurant != []:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #Form for renaming Restaurant name
        output = '''
            <html>
            <body>
                <h1>{}</h1>
                <form method='POST' enctype='multipart/form-data' action='/restaurants/{}/edit'>
                    <input name='new_name' type='text' placeholder="New Restaurant Name">
                    <input type='submit' value='Rename'>
                </form>
            </body>
            </html>
            '''.format(restaurant.name, str(restaurant.id))

        self.wfile.write(output)
        print(output)
    return


def OpenDeletePage(self):
    #Get the restaurant id from the path
    path_elements = self.path.split('/')
    id_string = path_elements[len(path_elements) - 2]
    restaurant_id = int(id_string)

    #Find restaurant to edit
    restaurant = _session.query(Restaurant).filter_by(id = restaurant_id).first()

    if restaurant != []:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #Form for deleting Restaurant
        output = '''
            <html>
            <body>
                <h1>Are you sure you want to delete {}?</h1>
                <form method='POST' enctype='multipart/form-data' action='/restaurants/{}/delete'>
                    <input type='submit' value='Delete'>
                </form>
            </body>
            </html>
            '''.format(restaurant.name, str(restaurant.id))

        self.wfile.write(output)
        print(output)
    return


def CreateNewRestaurant(self):
    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        fields = cgi.parse_multipart(self.rfile, pdict)
        input = fields.get('new_restaurant')

    new_entry = Restaurant(name = input[0])
    _session.add(new_entry)
    _session.commit()

    self.send_response(301)
    self.send_header('Content-type', 'text/html')
    self.send_header('Location', '/restaurants')
    self.end_headers()

    return


def EditRestaurantName(self):
    #Get the new name
    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        fields = cgi.parse_multipart(self.rfile, pdict)
        input = fields.get('new_name')

    #Get the restaurant id from the path
    path_elements = self.path.split('/')
    id_string = path_elements[len(path_elements) - 2]
    restaurant_id = int(id_string)

    #Find restaurant to edit
    restaurant = _session.query(Restaurant).filter_by(id = restaurant_id).first()

    #Update restaurant name
    if restaurant != []:
        restaurant.name = input[0]
        _session.add(restaurant)
        _session.commit()

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

    return


def DeleteRestaurant(self):
    #Get the restaurant id from the path
    path_elements = self.path.split('/')
    id_string = path_elements[len(path_elements) - 2]
    restaurant_id = int(id_string)

    #Find restaurant to delete
    restaurant = _session.query(Restaurant).filter_by(id = restaurant_id).first()

    #Delete restaurant
    if restaurant != []:
        _session.delete(restaurant)
        _session.commit()

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

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

            if self.path.endswith("/edit"):
                OpenEditPage(self)
                return

            if self.path.endswith("/delete"):
                OpenDeletePage(self)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                CreateNewRestaurant(self)
                return

            if self.path.endswith("/edit"):
                EditRestaurantName(self)
                return

            if self.path.endswith("/delete"):
                DeleteRestaurant(self)
                return

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