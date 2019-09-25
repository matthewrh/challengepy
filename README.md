# Penn Labs Server Challenge
**IMPORTANT:** I've continued this project in my spare time because I really enjoyed working on it and wanted to keep refining and adding features. To view the code that was submitted by the deadline, please go [here](https://github.com/matthewrh/challengepy/tree/80f3ab07d93c505bd8a2596d70c485e7117df06c).


## Installation
1. Clone this repository. 
2. `cd` into the cloned repository.
3. Install `pipenv`
    * `brew install pipenv` if you're on a Mac.
    * `pip install --user --upgrade pipenv` for most other machines.
4. Install packages using `pipenv install`.
5. Install `mongodb`
    * `brew tap mongodb/brew`
    * `brew install mongodb-community@4.2`
6. Open a new terminal window and run mongoDB with `mongod --config /usr/local/etc/mongod.conf`.
7. Return to your original terminal and run with `pipenv run python3 index.py`.
    * If this is your first time running, the mongoDB database and collections will automatically be created.
    * Additionally, the app will scrape for existing clubs and generate a user for Jennifer if the collections are empty.

## Data Models
* Clubs have names, descriptions, tags, and a favorite counter.
* Users have usernames, hashed passwords, and a list of favorited clubs.
* All data types have unique identifiers generated automatically by mongoDB.

## Endpoints
* [GET `/api/clubs`](https://github.com/matthewrh/challengepy#get-apiclubs)
* [POST `/api/clubs`](https://github.com/matthewrh/challengepy#post-apiclubs)
* [GET `/api/clubs/{club_id}`](https://github.com/matthewrh/challengepy#get-apiclubsclub_id)
* [POST `/api/clubs/{club_id}/update`](https://github.com/matthewrh/challengepy#post-apiclubsclub_idupdate)
* [GET `/api/clubs/{club_id}/favorites`](https://github.com/matthewrh/challengepy#get-apiclubsclub_idfavorites)
* [POST `/api/clubs/filter`](https://github.com/matthewrh/challengepy#post-apiclubsfilter)
* [GET `/api/user/{username}`](https://github.com/matthewrh/challengepy#get-apiuserusername)
* [POST `/api/account/register`](https://github.com/matthewrh/challengepy#post-apiaccountregister)
* [POST `/api/account/login`](https://github.com/matthewrh/challengepy#post-apiaccountlogin)
* [POST `/api/account/logout`](https://github.com/matthewrh/challengepy#post-apiaccountlogout)
* [GET `/api/friends`](https://github.com/matthewrh/challengepy#get-apifriends)
* [GET `/api/friends/requests`](https://github.com/matthewrh/challengepy#get-apifriendsrequests)
* [POST `/api/friends/requests`](https://github.com/matthewrh/challengepy#post-apifriendsrequests)
* [POST `/api/friends/add`](https://github.com/matthewrh/challengepy#post-apifriendsadd)
* [POST `/api/friends/remove`](https://github.com/matthewrh/challengepy#post-apifriendsremove)
* [POST `/api/favorite/add`](https://github.com/matthewrh/challengepy#post-apifavoriteadd)
* [POST `/api/favorite/remove`](https://github.com/matthewrh/challengepy#post-apifavoriteremove)

## Functionality

### GET `/api/clubs`
* Functionality: Returns a list of clubs in JSON format.
* Access: Public

### POST `/api/clubs`
* Functionality: Creates a new club and returns a list of clubs in JSON format.
* Access: Public
* Content-Type: JSON (`application/json`)
* Required Keys: `name`, `description`, `tags`
* Example Request Body:
```javascript
{
    "name": "CIS Club",
    "description": "CIS Fan Club",
    "tags": ["CIS", "Fan"]
}
```

### GET `/api/clubs/{club_id}`
* Functionality: Returns a club's name, description, tags, and favorite count in JSON format.
* Access: Public

### POST `/api/clubs/{club_id}/update`
* Functionality: Updates an existing club's name, description, and/or tags and returns the information in JSON format.
* Access: Public
* Content-Type: JSON (`application/json`)
* Required Keys: `name`, `description`, `tags`
* Example Request Body:
```javascript
{
    "name": "CIS+EE Club",
    "description": "CIS+EE Fan Club",
    "tags": ["CIS", "EE", "Fan"]
}
```

### GET `/api/clubs/{club_id}/favorites`
* Functionality: Returns a list of users that have favorited the club in JSON format.
* Access: Public

### POST `/api/clubs/filter`
* Functionality: Returns a filtered list of clubs with descriptions that include at least one keyword in JSON format.
* Access: Public
* Content-Type: JSON (`application/json`)
* Required Keys: `keywords`
* Example Request Body:
```javascript
{
    "keywords": [
        "blockchain",
        "artificial intelligence"
    ]
}
```

### GET `/api/user/{username}`
* Functionality: Returns a user's information in JSON format.
* Access: Requires User Login
    * Username will appear if requesting user is not friends with {username}
    * Username and favorites will appear if requesting user is friends with {username}
    * Username, favorites, friends, and friend requests will appear if requesting user is {username}

### POST `/api/account/register`
* Functionality: Creates a new user.
* Access: Public
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `password`
* Example Request Body:
```javascript
{
    "username": "john",
    "password": "totallysecurepassword"
}
```

### POST `/api/account/login`
* Functionality: Logs a user in and creates a user session.
* Access: Public
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `password`
* Example Request Body:
```javascript
{
    "username": "jen",
    "password": "password123"
}
```

### POST `/api/account/logout`
* Functionality: Logs a user out and ends the user session.
* Access: Public

### GET `/api/friends`
* Functionality: Returns a list of user's friends as usernames in JSON format.
* Access: Requires User Login

### GET `/api/friends/requests`
* Functionality: Returns a list user's incoming and outgoing friend requests as usernames in JSON format.
* Access: Requires User Login

### POST `/api/friends/requests`
* Functionality: Accept, reject, or cancel friend requests and update corresponding values.
* Access: Requires User Login
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `friend_username`, `action` (Accepted Values: `accept`, `reject`, `cancel`)
* Example Request Body:
```javascript
{
    "username": "jen",
    "friend_username": "john",
    "action": "accept"
}
```

### POST `/api/friends/add`
* Functionality: Send a friend request to specified user.
* Access: Requires User Login
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `friend_username`
* Example Request Body:
```javascript
{
    "username": "jen",
    "friend_username": "john"
}
```

### POST `/api/friends/remove`
* Functionality: Remove a specified user from user's friends list.
* Access: Requires User Login
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `friend_username`
* Example Request Body:
```javascript
{
    "username": "jen",
    "friend_username": "john"
}
```

### POST `/api/favorite/add`
* Functionality: Add a club to user's favorites and increase the club's favorite count by one.
* Access: Requires User Login
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `club_id`
* Example Request Body:
```javascript
{
    "username": "jen"
    "club_id": "5d89858e6ed34aa6f41deb44"
}
```

### POST `/api/favorite/remove`
* Functionality: Remove a club from user's favorites and decrease the club's favorite count by one.
* Access: Requires User Login
* Content-Type: JSON (`application/json`)
* Required Keys: `username`, `club_id`
* Example Request Body:
```javascript
{
    "username": "jen"
    "club_id": "5d89858e6ed34aa6f41deb44"
}
```

## Additional Notes
* TODO: Error handling for when user is not logged in.
* TODO: DevOps/Server using Digital Ocean droplet or Heroku.
