# Restaurants

The restaurants application keeps a database of Restaurants and Menu Items for each restaurant.

## Prerequisites

1. python 3.6.3
2. sqlalchemy
3. sqlite3
4. _database_setup.py_ from the github repository [restaurants](https://github.com/czar3985/restaurants)
5. _webserver.py_ from the same restaurant

## Usage

The following resource gives more information on how to run python scripts: 
[How to Run a Python Script via a File or the Shell](https://www.pythoncentral.io/execute-python-script-file-shell/).

_database_setup.py_ will setup the database: _restaurantmenu.db_

_webserver.py_ will run the web server. 

Navigate to port 8080, restaurants page of the server PC
Ex: http://SERVERPC:8080/restaurants/

## Database Structure

```
Table Name: restaurant
Columns:
{'primary_key': 0, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=250), 'name': u'name'}
{'primary_key': 1, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'id'}

Table Name: menu_item
Columns:
{'primary_key': 0, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=80), 'name': u'name'}
{'primary_key': 1, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'id'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=250), 'name': u'description'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=8), 'name': u'price'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=250), 'name': u'course'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'restaurant_id'}
```

## To Do

Coding ongoing
