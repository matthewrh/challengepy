# Penn Labs Server Challenge
**IMPORTANT:** I've continued this project in my spare time because I really enjoyed working on it and wanted to keep refining and adding features. To view the code that was submitted by the deadline, please go [here](https://github.com/matthewrh/challengepy/tree/80f3ab07d93c505bd8a2596d70c485e7117df06c).

## Information
This project was completed as a technical challenge submission for my Penn Labs Fall 2019 application. I completed the server challenge (found [here](https://www.notion.so/Server-Challenge-Fall-19-480abf1871fc4a8d9600154816726343)).

### Additional Features
In addition to the required elements of the challenge, I also implemented the following:
* User (register, login, logout)
    * Rationale: This feature adds the benefit of having a built-in method for creating new users. It also allowed me to set permissions for various endpoints based on a user's status.
    * Notes: Users provide their own password when registering which is then hashed and stored using SHA256 within PBKDF2. The password is checked every time the user logs in. A user session is created upon login which remains active until the user logs out.
* Friends (Add, remove, accept request, reject request, cancel request, list, request list)
    * Rationale: Users now have the ability to add friends. By adding a friend, a user is able to view that friend's favorite clubs.
    * Notes: Adding a friend sends a friend request to the specified user which can be accepted or rejected. Users will not be added to eachother's friend lists unless the request is accepted. The sending user also has the ability to cancel their request. Users can remove friends at any time.
* Club (info, update, favorite list, filter)
    * Rationale: Users can now search through the clubs database using keywords, view info for a specific club, and view a list of users who have favorited a specific club. Administrators also have the ability to update information for existing clubs.
    * Notes: Keywords are searched for independently, meaning not all keywords must be present in a club's description for the club to be included in the results. Administrators are hard-coded by username. For the purpose of this challenge, Jennifer (`jen`) is listed as an administrator.

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
    * Additionally, the app will scrape for existing clubs and generate a user for Jennifer (`jen`) if the collections are empty.

## Data Models
* Clubs have names, descriptions, tags, and a favorite counter.
* Users have usernames, hashed passwords, a list of friends, a list of friend requests, and a list of favorited clubs.
* All data types have unique identifiers generated automatically by mongoDB.

## Endpoints
* [GET `/`](https://github.com/matthewrh/challengepy#get-)
* [GET `/api`](https://github.com/matthewrh/challengepy#get-api)
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

### GET `/`
* Access: Public

### GET `/api`
* Access: Public

### GET `/api/clubs`
* Functionality: Returns a list of clubs in JSON format.
* Access: Public

### POST `/api/clubs`
* Functionality: Creates a new club and returns a list of clubs in JSON format.
* Access: Requires User Login
    * User must be administrator
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
* Access: Requires User Login
    * User must be administrator
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
* TODO: Comments: Allow users to add, delete, and view comments for clubs.
* TODO: Ratings: Allow users to rate and view average ratings for clubs.
* TODO: Error handling for when client attempts to access a user-only resources while not logged in.
* TODO: DevOps/Server using Digital Ocean droplet or Heroku.
