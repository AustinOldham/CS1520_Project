from google.cloud import datastore

import hashlib

# This code is based on the code found at https://github.com/timothyrjames/cs1520 with permission from the instructor

# Everyone will likely have a different project ID. Put yours here so the
# datastore stuff works
_PROJECT_ID = 'roommate-tinder'
_USER_ENTITY = 'roommate_user'


class User(object):
    def __init__(self, username, email='', about='', firstname='', lastname='', age='', gender='', bio='', liked_users=[]):
        self.username = username
        self.email = email
        self.about = about
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.bio = bio
        self.liked_users = liked_users

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
            'liked_users': self.liked_users
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
        return User(username=user['username'], email=user['email'], about=user['about'], firstname=user['firstname'], lastname=user['lastname'], age=user['age'], gender=user['gender'], bio=user['bio'])
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
        return User(username=user['username'], about=user['about'], firstname=user['firstname'], lastname=user['lastname'], age=user['age'], gender=user['gender'], bio=user['bio'])
    else:
        return ''


def save_user_profile(username, firstname, lastname, age, gender, about, bio):
    """Save the user profile info to the datastore."""

    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    user['firstname'] = firstname
    user['lastname'] = lastname
    user['age'] = age
    user['gender'] = gender
    user['about'] = about
    user['bio'] = bio
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


def like_user(username, other_username):
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    liked_list = get_liked_users(username)
    liked_list.append(other_username)
    user['liked_users'] = liked_list
    client.put(user)


def unlike_user(username, other_username):
    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    liked_list = get_liked_users(username)
    liked_list.remove(other_username)
    user['liked_users'] = liked_list
    client.put(user)


def get_liked_users(username):
    user = _load_entity(_get_client(), _USER_ENTITY, username)
    return user['liked_users']


# TODO: Make the liked users list a hashtable in order to speed up the search.
def make_match(username):
    """Matches with a random user"""
    client = _get_client()
    q = client.query(kind=_USER_ENTITY)
    liked_list = get_liked_users(username)
    results = list(q.fetch())
    # results = list(q.fetch(100))  # Adds a limit to the maximum number of results
    print(results)
    for user in results:
        print("RESULT (d): " + user['username'])
        print("RESULT (o): " + user.username)
        if (user['username'] != username and user['username'] not in liked_list):
            return user['username']
    return ''


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
    entity['bio'] = ''
    entity['liked_users'] = []
    client.put(entity)


def save_about_user(username, about):
    """Save the user's about info to the datastore."""

    client = _get_client()
    user = _load_entity(client, _USER_ENTITY, username)
    user['about'] = about
    client.put(user)


def create_data():
    """You can use this function to populate the datastore with some basic
    data."""

    client = _get_client()
    entity = datastore.Entity(client.key(_USER_ENTITY, 'testuser'),
                              exclude_from_indexes=[])
    entity.update({
        'username': 'testuser',
        'passwordhash': '',
        'email': '',
        'about': '',
        # 'completions': [],
    })
    client.put(entity)


def get_password_hash(pw):
    """This will give us a hashed password that will be extremlely difficult to
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""

    encoded = pw.encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()
