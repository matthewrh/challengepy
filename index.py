from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from scraper import *
import json

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'pcrdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pcrdb'
app.secret_key = 'pennlabs'

login = LoginManager(app)
login.login_view = 'login'

mongo = PyMongo(app)





class Club(object):
    def __init__(self, name, description, tags):
        if not clubs.find_one({'name': name}):
            self.name = name
            self.description = description
            self.tags = tags
            self.favorite_count = 0

            self.insert()
        else:
            existing_info = clubs.find_one({'name': name})
            self.name = name
            self.description = existing_info['description']
            self.tags = existing_info['tags']
            self.favorite_count = existing_info['favorite_count']
    
    def get_name(self):
        return self.name
    
    def json_club(self):
        return {
            'name': self.get_name()
        }

    def insert(self):
        if not clubs.find_one({'name': self.name}):
            clubs.insert_one(self.json())
        else:
            clubs.update_one(self.json_club(), {'$set': self.json()})

    def json(self):
        if not clubs.find_one({'name': self.name}):
            return {
                'name': self.name,
                'description': self.description,
                'tags': self.tags,
                'favorite_count': self.favorite_count
            }
        else:
            existing_doc = clubs.find_one({'name': self.name})
            return {
                '_id': existing_doc['_id'],
                'name': self.name,
                'description': self.description,
                'tags': self.tags,
                'favorite_count': self.favorite_count
            }
    
    def add_fav(self):
        self.favorite_count += 1
        self.insert()
        return 'favorite count updated'
    
    def remove_fav(self):
        self.favorite_count -= 1
        self.insert()
        return 'favorite count updated'




class User(object):
    def __init__(self, username, password):
        if not users.find_one({'username': username}):
            self.username = username
            self.password_hash = generate_password_hash(password)
            self.favorites = []

            self.insert()
        else:
            existing_info = users.find_one({'username': username})
            self.username = username
            self.password_hash = existing_info['password_hash']
            self.favorites = existing_info['favorites']
    
    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username
    
    def json_user(self):
        return {
            'username': self.get_id()
        }
    
    def insert(self):
        if not users.find_one({'username': self.username}):
            users.insert_one(self.json())
        else:
            users.update_one(self.json_user(), {'$set': self.json()})

    def json(self):
        if not users.find_one({'username': self.username}):
            return {
                'username': self.username,
                'password_hash': self.password_hash,
                'favorites': self.favorites
            }
        else:
            existing_doc = users.find_one({'username': self.username})
            return {
                '_id': existing_doc['_id'],
                'username': self.username,
                'password_hash': self.password_hash,
                'favorites': self.favorites
            }

    def json_public(self):
        favorites_list = []
        for i in self.favorites:
            fav_find = clubs.find_one({'_id': ObjectId(i)})
            favorites_list.append(fav_find['name'])
        return {
            'username': self.username,
            'favorites': favorites_list
        }
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_favorite(self, favorite):
        if not favorite in self.favorites:
            self.favorites.append(favorite)
            self.insert()

            clubby = clubs.find_one({'_id': ObjectId(favorite)})
            c = Club(clubby['name'], '', '')
            c.add_fav()
            return 'favorite added successfully'
        else:
            return 'already favorited'

    def remove_favorite(self, favorite):
        if favorite in self.favorites:
            self.favorites.remove(favorite)
            self.insert()

            clubby = clubs.find_one({'_id': ObjectId(favorite)})
            c = Club(clubby['name'], '', '')
            c.remove_fav()
            return 'favorite removed successfully'
        else:
            return 'club not favorited'





clubs = mongo.db.clubs
if clubs.estimated_document_count() == 0:
    data = get_club_list()
    for i in data:
        Club(i['name'], i['description'], i['tags'])

users = mongo.db.users
if users.estimated_document_count() == 0:
    User('jen', 'password123')

@login.user_loader
def load_user(username):
    u = users.find_one({"username": username})
    if not u:
        return None
    return User(username, '')

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET'])
def list_clubs():
    clubs_list = clubs.find()
    return json_util.dumps(clubs_list)

@app.route('/api/clubs', methods=['POST'])
def add_club():
    if request.json:
        Club(request.json['name'], request.json['description'], request.json['tags'])
        clubs_list = clubs.find()
        return json_util.dumps(clubs_list)
    else:
        return 'invalid request'

@app.route('/api/user/<uname>/', methods=['GET'])
def get_user(uname):
    pub = User(uname, '')
    return json_util.dumps(pub.json_public())

@app.route('/api/account/register', methods=['POST'])
def add_user():
    if request.json:
        User(request.json['username'], request.json['password'])
        return 'registered successfully. please proceed to login.'
    else:
        return 'invalid request'

@app.route('/api/account/login', methods=['POST'])
def user_login():
    if request.json:
        if current_user.is_authenticated:
            return 'already logged in'
        if users.find_one({'username': request.json['username']}):
            login = User(request.json['username'], request.json['password'])
            if login.check_password(request.json['password']):
                login_user(login)
                return 'login successful'
            else:
                return 'incorrect password'
        else:
            return 'no account found with provided username'
    else:
        return 'invalid request'

@app.route('/api/account/logout', methods=['POST'])
def user_logout():
    if current_user.is_authenticated:
        logout_user()
        return 'logout successful'
    else:
        return 'not logged in'

@app.route('/api/favorite/add', methods=['POST'])
@login_required
def add_fav():
    if request.json:
        if clubs.find_one({'_id': ObjectId(request.json['club_id'])}):
            user = User(request.json['username'], '')
            if user.add_favorite(request.json['club_id']) == 'already favorited':
                return 'already favorited'
            return 'favorite added successfully'
        else:
            'club does not exist'
    else:
        return 'invalid request'

@app.route('/api/favorite/remove', methods=['POST'])
@login_required
def remove_fav():
    if request.json:
        if clubs.find_one({'_id': ObjectId(request.json['club_id'])}):
            user = User(request.json['username'], '')
            if user.remove_favorite(request.json['club_id']) == 'club not favorited':
                return 'club not favorited'
            return 'favorite removed successfully'
        else:
            'club does not exist'
    else:
        return 'invalid request'

if __name__ == '__main__':
    app.run()
