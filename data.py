from google.cloud import datastore
from datetime import datetime, timezone, timedelta

import hashlib
import json
import random


# This code is based on the code found at https://github.com/timothyrjames/cs1520 with permission from the instructor

# Everyone will likely have a different project ID. Put yours here so the
# datastore stuff works
_PROJECT_ID = 'roommate-tinder'
_USER_ENTITY = 'roommate_user'

MAX_LIKED_TIME = timedelta(days=30)


class User(object):
    def __init__(self, username, email='', about='', firstname='', lastname='', age='', gender='', state='', city='', address='', bio='', liked_users='', avatar=''):
        self.username = username
        self.email = email
        self.about = about
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.state = state
        self.city = city
        self.address = address
        self.bio = bio
        self.liked_users = liked_users
        self.avatar = avatar

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'about': self.about,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender,
            'bio': self.bio,
            'liked_users': self.liked_users,
            'avatar': self.avatar
        }


def _get_client():
    """Returns the datastore client"""

    return datastore.Client(_PROJECT_ID)


def _load_key(client, entity_type, entity_id=None, parent_key=None):
    """Load a datastore key using a particular client, and if known, the ID.  Note
    that the ID should be an int - we're allowing datastore to generate them in
    this example."""

    key = None
    if entity_id:
        key = client.key(entity_type, entity_id, parent=parent_key)
    else:
        # this will generate an ID
        key = client.key(entity_type)
    return key


def _load_entity(client, entity_type, entity_id, parent_key=None):
    """Load a datstore entity using a particular client, and the ID."""

    key = _load_key(client, entity_type, entity_id, parent_key)
    entity = client.get(key)
    # log('retrieved entity for ' + str(entity_id))
    return entity


def load_user(username, passwordhash):
    """Load a user based on the passwordhash; if the passwordhash doesn't match
    the username, then this should return None."""

    client = _get_client()
    q = client.query(kind=_USER_ENTITY)
    q.add_filter('username', '=', username)
    q.add_filter('passwordhash', '=', passwordhash)
    for user in q.fetch():
        return User(username=user['username'], email=user['email'], about=user['about'], firstname=user['firstname'], lastname=user['lastname'], age=user['age'], gender=user['gender'], state=user['state'], city=user['city'], address=user['address'], bio=user['bio'], liked_users=user['liked_users'], avatar=user['avatar'])
    return None


# Note: This may be removed in the future
def load_about_user(username):
    """Return a string that represents the "About Me" information a user has
    stored."""

    user = _load_entity(_get_client(), _USER_ENTITY, username)
    if user:
        return user['about']
    else:
        return ''


def load_public_user(username):
    """Returns a user object that contains information that anyone can view."""

    user = _load_entity(_get_client(), _USER_ENTITY, username)
    if user:
        return User(username=user['username'], about=user['about'], firstname=user['firstname'], lastname=user['lastname'], age=user['age'], gender=user['gender'], state=user['state'], city=user['city'], address=user['address'], bio=user['bio'], avatar=user['avatar'])
    else:
        return ''


def save_user_profile(username, firstname, lastname, age, gender, city, state, address, about, bio, avatar):
    """Save the user profile info to the datastore."""

    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    user['firstname'] = firstname
    user['lastname'] = lastname
    user['age'] = age
    user['gender'] = gender
    user['state'] = state
    user['city'] = city
    user['address'] = address
    user['about'] = about
    user['bio'] = bio
    user['avatar'] = avatar
    client.put(user)


#def test_add_liked_users(username):
#    client = _get_client()
#    entity = datastore.Entity(_load_key(client, _USER_ENTITY, username))
#    entity['liked_users'] = ["test1", "test2", "test3"]
#    client.put(entity)


#def test_return_liked_users(username):
#    user = _load_entity(_get_client(), _USER_ENTITY, username)
#    liked = user['liked_users']
#    return (liked[2] + liked[1] + liked[0])

def is_like_expired(old_date_string):
    """Checks how long ago the like was made"""
    old_date = datetime.strptime(old_date_string, "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now(timezone.utc)
    difference = current_date - old_date
    return difference > MAX_LIKED_TIME


def like_user(username, other_username):
    current_time = datetime.now(timezone.utc)  # Uses UTC for consistency.
    liked_dict = get_liked_users(username)
    liked_dict[other_username] = current_time.isoformat(' ', 'seconds')  # Stores the time that the like was performed in order to allow the program to remove old entries.
    save_liked_users(liked_dict, username)


def unlike_user(username, other_username):
    liked_dict = get_liked_users(username)
    del liked_dict[other_username]
    save_liked_users(liked_dict, username)


# If the json conversion is too slow, use ujson
def get_liked_users(username):
    user = _load_entity(_get_client(), _USER_ENTITY, username)
    liked_dict = json.loads(user['liked_users'] or '{}')  # Converts the json string to a dictionary.
    return liked_dict


def save_liked_users(liked_dict, username):
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    user['liked_users'] = json.dumps(liked_dict)  # Converts the dictionary to a string since Datastore does not support dictionaries.
    client.put(user)


def make_match(username):
    """Matches with a random user"""
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)

    q = client.query(kind=_USER_ENTITY)
    q.add_filter('state', '=', user['state'])
    q.add_filter('city', '=', user['city'])

    liked_dict = get_liked_users(username)
    results = list(q.fetch(100))  # Adds a limit to the maximum number of results
    for potential_match in results:
        if (potential_match['username'] not in liked_dict and potential_match['username'] != username):
            return potential_match['username']
    return ''


def get_all_locations():
    """Lookup all user locations for google maps"""
    client = _get_client()
    q = client.query(kind=_USER_ENTITY)

    results = list(q.fetch())
    return results


def save_new_user(user, passwordhash):
    """Save the user details to the datastore."""

    client = _get_client()
    entity = datastore.Entity(_load_key(client, _USER_ENTITY, user.username))
    entity['username'] = user.username
    entity['email'] = user.email
    entity['passwordhash'] = passwordhash
    entity['about'] = ''
    entity['firstname'] = ''
    entity['lastname'] = ''
    entity['age'] = ''
    entity['gender'] = ''
    entity['state'] = ''
    entity['city'] = ''
    entity['address'] = ''
    entity['bio'] = ''
    entity['liked_users'] = ''
    entity['avatar'] = ''
    client.put(entity)


def save_about_user(username, about):
    """Save the user's about info to the datastore."""

    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    user['about'] = about
    client.put(user)


def create_data(num=50, state='PA', city='Pittsburgh'):
    """You can use this function to populate the datastore with some basic
    data."""

    random_id = random.randint(0, 2147483647)

    for i in range(num):
        client = _get_client()
        entity = datastore.Entity(_load_key(client, _USER_ENTITY, 'sample_username{}_{}'.format(random_id, i)))
        entity['username'] = 'sample_username{}_{}'.format(random_id, i)
        entity['email'] = 'sample_email{}@example.com'.format(i)
        entity['passwordhash'] = get_password_hash(str(i))
        entity['about'] = 'Sample about section {}'.format(i)
        entity['firstname'] = 'First{}'.format(i)
        entity['lastname'] = 'Last{}'.format(i)
        entity['age'] = str(i)
        entity['gender'] = 'gender{}'.format(i)
        entity['state'] = state
        entity['city'] = city
        entity['address'] = str(random.randint(0, 6000)) + ' Forbes Avenue'
        entity['bio'] = 'Sample bio {}'.format(i)
        entity['liked_users'] = ''
        entity['avatar'] = 'mushroom.png'
        client.put(entity)


def get_password_hash(pw):
    """This will give us a hashed password that will be extremlely difficult to
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""

    encoded = pw.encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()
