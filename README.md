# Penn Labs Server Challenge
Remember to **document your work** in this `README.md` file! Feel free to delete these installation instructions in your fork of this repository.

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

## Functionality
* GET `/api/clubs` will return the list of clubs in json.
* GET `/api/user/<username>` will return a user and their list of favorites.
* POST `/api/clubs` in json with keys `name`, `description`, and `tags` will add a new club.
* POST `/api/account/register` in json with keys `username` and `password` will create a new user. The password will be hashed.
* POST `/api/account/login` in json with keys `username` and `password` will log a user in.
* POST `/api/account/logout` in json will log a user out.
* POST `/api/favorite/add` in json with keys `username` and `club_id` will add a club to user's favorites and increase the club's total favorites by one. NOTE: Requires user to be logged in.
* POST `/api/favorite/remove` in json with keys `username` and `club_id` will remove a club from user's favorites and decrease the club's total favorites by one. NOTE: Requires user to be logged in.

## Additional Notes
* TODO: Allow clubs to be queried and filtered using keywords.
* TODO: Pull information for a specific club using club's id.
