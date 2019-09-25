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
    def __init__(self, name, description, tags, cid):
        if not clubs.find_one({'name': name}) and not name == '' and cid == '':
            self.name = name
            self.description = description
            self.tags = tags
            self.favorite_count = 0

            self.insert()

            existing_info = clubs.find_one({'name': self.name, 'description': self.description, 'tags': self.tags})
            self.cid = existing_info['_id']
        elif cid == '' and not name == '':
            existing_info = clubs.find_one({'name': name})
            self.name = existing_info['name']
            self.description = existing_info['description']
            self.tags = existing_info['tags']
            self.cid = existing_info['_id']
            self.favorite_count = existing_info['favorite_count']
        elif clubs.find_one({'_id': ObjectId(cid)}) and not name == '' and not description == '' and not tags == '':
            existing_info = clubs.find_one({'_id': ObjectId(cid)})
            self.name = name
            self.description = description
            self.tags = tags
            self.cid = existing_info['_id']
            self.favorite_count = existing_info['favorite_count']

            self.insert()
        elif clubs.find_one({'_id': ObjectId(cid)}):
            existing_info = clubs.find_one({'_id': ObjectId(cid)})
            self.name = existing_info['name']
            self.description = existing_info['description']
            self.tags = existing_info['tags']
            self.cid = existing_info['_id']
            self.favorite_count = existing_info['favorite_count']
        else:
            existing_info = clubs.find_one({'name': name})
            self.name = name
            self.description = existing_info['description']
            self.tags = existing_info['tags']
            self.cid = existing_info['_id']
            self.favorite_count = existing_info['favorite_count']
    
    def get_cid(self):
        return self.cid
    
    def json_club(self):
        return {
            '_id': self.get_cid()
        }

    def insert(self):
        if not hasattr(self, 'cid'):
            clubs.insert_one(self.json())
        elif not clubs.find_one({'_id': self.cid}):
            clubs.insert_one(self.json())
        else:
            clubs.update_one(self.json_club(), {'$set': self.json()})

    def json(self):
        if not hasattr(self, 'cid'):
            return {
                'name': self.name,
                'description': self.description,
                'tags': self.tags,
                'favorite_count': self.favorite_count
            }
        elif not clubs.find_one({'_id': self.cid}):
            return {
                'name': self.name,
                'description': self.description,
                'tags': self.tags,
                'favorite_count': self.favorite_count
            }
        else:
            existing_doc = clubs.find_one({'_id': self.cid})
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
            self.friends = []
            self.friend_requests = []
            self.favorites = []

            self.insert()
        else:
            existing_info = users.find_one({'username': username})
            self.username = username
            self.password_hash = existing_info['password_hash']
            self.friends = existing_info['friends']
            self.friend_requests = existing_info['friend_requests']
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
                'favorites': self.favorites,
                'friends': self.friends,
                'friend_requests': self.friend_requests
            }
        else:
            existing_doc = users.find_one({'username': self.username})
            return {
                '_id': existing_doc['_id'],
                'username': self.username,
                'password_hash': self.password_hash,
                'favorites': self.favorites,
                'friends': self.friends,
                'friend_requests': self.friend_requests
            }

    def json_public(self, session_username):
        favorites_list = []
        for i in self.favorites:
            fav_find = clubs.find_one({'_id': ObjectId(i)})
            favorites_list.append(fav_find['name'])
        if session_username == self.username:
            return {
                'username': self.username,
                'favorites': self.favorites,
                'friends': self.friends,
                'friend_requests': self.friend_requests
            }
        elif session_username in self.friends:
            return {
                'username': self.username,
                'favorites': favorites_list
            }
        else:
            return {
                'username': self.username
            }
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def accept_friend_request(self, friend_username):
        req1 = {
            'username': friend_username,
            'type': 'incoming'
        }
        req2 = {
            'username': self.username,
            'type': 'outgoing'
        }
        if req1 in self.friend_requests:
            self.friend_requests.remove(req1)
            self.friends.append(friend_username)
            self.insert()

            f = User(friend_username, '')
            f.friend_requests.remove(req2)
            f.friends.append(self.username)
            f.insert()
            return 'friend request accepted'
        else:
            return 'no friend request from this user exists'

    def reject_friend_request(self, friend_username):
        req1 = {
            'username': friend_username,
            'type': 'incoming'
        }
        req2 = {
            'username': self.username,
            'type': 'outgoing'
        }
        if req1 in self.friend_requests:
            self.friend_requests.remove(req1)
            self.insert()

            f = User(friend_username, '')
            f.friend_requests.remove(req2)
            f.insert()
            return 'friend request rejected'
        else:
            return 'no friend request from this user exists'

    def cancel_friend_request(self, friend_username):
        req1 = {
            'username': friend_username,
            'type': 'outgoing'
        }
        req2 = {
            'username': self.username,
            'type': 'incoming'
        }
        if req1 in self.friend_requests:
            self.friend_requests.remove(req1)
            self.insert()

            f = User(friend_username, '')
            f.friend_requests.remove(req2)
            f.insert()
            return 'friend request cancelled'
        else:
            return 'no friend request to this user exists'

    def add_friend(self, friend_username):
        req1 = {
            'username': friend_username,
            'type': 'outgoing'
        }
        req2 = {
            'username': self.username,
            'type': 'incoming'
        }
        req3 = {
            'username': friend_username,
            'type': 'incoming'
        }
        if req3 in self.friend_requests:
            return 'you already have a pending friend request from this user'
        elif not req1 in self.friend_requests and not friend_username in self.friends:
            self.friend_requests.append(req1)
            self.insert()

            f = User(friend_username, '')
            f.friend_requests.append(req2)
            f.insert()
            return 'friend request sent'
        elif req1 in self.friend_requests:
            return 'friend request already sent'
        elif friend_username in self.friends:
            return 'already friends with this user'
        else:
            return 'err'
    
    def remove_friend(self, friend_username):
        if friend_username in self.friends:
            self.friends.remove(friend_username)
            self.insert()

            f = User(friend_username, '')
            f.friends.remove(self.username)
            f.insert()
            return 'friend removed successfully'
        else:
            return 'not friends with this user'

    def add_favorite(self, favorite):
        if not favorite in self.favorites:
            self.favorites.append(favorite)
            self.insert()

            clubby = clubs.find_one({'_id': ObjectId(favorite)})
            c = Club(clubby['name'], '', '', '')
            c.add_fav()
            return 'favorite added successfully'
        else:
            return 'already favorited'

    def remove_favorite(self, favorite):
        if favorite in self.favorites:
            self.favorites.remove(favorite)
            self.insert()

            clubby = clubs.find_one({'_id': ObjectId(favorite)})
            c = Club(clubby['name'], '', '', '')
            c.remove_fav()
            return 'favorite removed successfully'
        else:
            return 'club not favorited'





clubs = mongo.db.clubs
if clubs.estimated_document_count() == 0:
    data = get_club_list()
    for i in data:
        Club(i['name'], i['description'], i['tags'], '')

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
        clubs_list = clubs.find()
        for i in clubs_list:
            if i['name'].lower() == request.json['name'].lower():
                return 'club already exists with this name'
        Club(request.json['name'], request.json['description'], request.json['tags'], '')
        clubs_list = clubs.find()
        return json_util.dumps(clubs_list)
    else:
        return 'invalid request'

@app.route('/api/clubs/<club_id>/', methods=['GET'])
def get_club_info(club_id):
    pub = Club('', '', '', club_id)
    return json_util.dumps(pub.json())

@app.route('/api/clubs/<club_id>/update', methods=['POST'])
def update_club(club_id):
    if request.json:
        eclub = clubs.find_one({"_id": ObjectId(club_id)})
        nname = eclub['name']
        ndesc = eclub['description']
        ntags = eclub['tags']
        if not nname == request.json['name']:
            nname = request.json['name']
        if not ndesc == request.json['description']:
            ndesc = request.json['description']
        if not ntags == request.json['tags']:
            ntags = request.json['tags']
        pub = Club(nname, ndesc, ntags, club_id)
        return json_util.dumps(pub.json())
    else:
        return 'invalid request'

@app.route('/api/clubs/<club_id>/favorites', methods=['GET'])
def get_club_favorites(club_id):
    users_list = users.find()
    users_shortlist = []
    for i in users_list:
        for j in i['favorites']:
            if club_id == j:
                users_shortlist.append(i['username'])
    return json_util.dumps(users_shortlist)

@app.route('/api/clubs/filter', methods=['POST'])
def filter_clubs():
    if request.json:
        clubs_list = clubs.find()
        clubs_shortlist = []
        for i in clubs_list:
            for j in request.json['keywords']:
                if j.lower() in i['description'].lower():
                    if i not in clubs_shortlist:
                        clubs_shortlist.append(i)
        return json_util.dumps(clubs_shortlist)
    else:
        return 'invalid request'

@app.route('/api/user/<uname>/', methods=['GET'])
@login_required
def get_user(uname):
    pub = User(uname, '')
    return json_util.dumps(pub.json_public(current_user.username))

@app.route('/api/account/register', methods=['POST'])
def add_user():
    if request.json:
        if not current_user.is_authenticated:
            users_list = users.find()
            for i in users_list:
                if i['username'].lower() == request.json['username'].lower():
                    return 'username already exists'
            User(request.json['username'], request.json['password'])
            return 'registered successfully. please proceed to login.'
        else:
            return 'can\'t create an account while logged in'
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

@app.route('/api/friends', methods=['GET'])
@login_required
def list_friends():
    users_list = users.find()
    for i in users_list:
        if i['username'] == current_user.username:
            return json_util.dumps(i['friends'])
    return 'insufficient permissions'

@app.route('/api/friends/requests', methods=['GET'])
@login_required
def list_friend_requests():
    users_list = users.find()
    for i in users_list:
        if i['username'] == current_user.username:
            return json_util.dumps(i['friend_requests'])
    return 'insufficient permissions'

@app.route('/api/friends/requests', methods=['POST'])
@login_required
def manage_friend_requests():
    if request.json:
        if current_user.username == request.json['username']:
            if users.find_one({'username': request.json['friend_username']}):
                user = User(request.json['username'], '')
                if request.json['action'] == 'accept':
                    return user.accept_friend_request(request.json['friend_username'])
                elif request.json['action'] == 'reject':
                    return user.reject_friend_request(request.json['friend_username'])
                elif request.json['action'] == 'cancel':
                    return user.cancel_friend_request(request.json['friend_username'])
                else:
                    return 'invalid action (accepted actions: accept, reject, cancel)'
            else:
                return 'user does not exist'
        else:
            return 'insufficient permissions'
    else:
        return 'invalid request'

@app.route('/api/friends/add', methods=['POST'])
@login_required
def send_friend_request():
    if request.json:
        if current_user.username == request.json['username']:
            if users.find_one({'username': request.json['friend_username']}):
                user = User(request.json['username'], '')
                return user.add_friend(request.json['friend_username'])
            else:
                return 'user does not exist'
        else:
            return 'insufficient permissions'
    else:
        return 'invalid request'

@app.route('/api/friends/remove', methods=['POST'])
@login_required
def remove_friend():
    if request.json:
        if current_user.username == request.json['username']:
            if users.find_one({'username': request.json['friend_username']}):
                user = User(request.json['username'], '')
                return user.remove_friend(request.json['friend_username'])
            else:
                return 'user does not exist'
        else:
            return 'insufficient permissions'
    else:
        return 'invalid request'

@app.route('/api/favorite/add', methods=['POST'])
@login_required
def add_fav():
    if request.json:
        if current_user.username == request.json['username']:
            if clubs.find_one({'_id': ObjectId(request.json['club_id'])}):
                user = User(request.json['username'], '')
                return user.add_favorite(request.json['club_id'])
            else:
                return 'club does not exist'
        else:
            return 'insufficient permissions'
    else:
        return 'invalid request'

@app.route('/api/favorite/remove', methods=['POST'])
@login_required
def remove_fav():
    if request.json:
        if current_user.username == request.json['username']:
            if clubs.find_one({'_id': ObjectId(request.json['club_id'])}):
                user = User(request.json['username'], '')
                return user.remove_favorite(request.json['club_id'])
            else:
                return 'club does not exist'
        else:
            return 'insufficient permissions'
    else:
        return 'invalid request'

if __name__ == '__main__':
    app.run()
