from flask import render_template, request, session, redirect
from email.utils import parseaddr
from main import app
import data

# Part of this code is based on the code found at https://github.com/timothyrjames/cs1520 with permission from the instructor


@app.route('/')
@app.route('/index.html')
def root():
	return render_template('index.html', page_title='Home')


@app.route('/signup.html')
def signup():
	return render_template('signup.html', page_title='Sign Up')


@app.route('/signin.html')
def signin():
	return render_template('signin.html', page_title='Sign In')


@app.route('/editprofile.html')
def editprofile():
	return render_template('editprofile.html', page_title='Edit Profile')


@app.route('/signin_user', methods=['POST'])
def signin_user():
	username = request.form.get('username')
	password = request.form.get('password')
	passwordhash = data.get_password_hash(password)
	user = data.load_user(username, passwordhash)
	if user:
		session['user'] = user.username
		return redirect('/profile/{}'.format(username))
	else:
		# return show_login_page()
		return redirect('/signin.html')


# TODO: Add check if the current username is in the liked list and pass a variable to the page so a conditional block can correctly choose between a "Like" and an "Unlike" button
@app.route('/profile/<username>')
def profile_page(username):
	user = data.load_public_user(username)
	current_user = session['user']
	is_owner = False  # Checks if the user is looking at his own profile
	if current_user == user.username:
		is_owner = True
	liked_list = data.get_liked_list(current_user)
	is_liked = False
	if username in liked_list:
		is_liked = True
	return render_template('profile.html', page_title=username, name_text=("{} {}".format(user.firstname, user.lastname)), gender_text=user.gender, age_text=str(user.age), about_text=user.about, bio_text=user.bio, other_username=user.username, is_owner=is_owner, is_liked=is_liked)


# TODO: Ensure that the username is unique
@app.route('/register', methods=['POST'])
def register_user():
	username = request.form.get('username')
	password1 = request.form.get('password1')
	password2 = request.form.get('password2')
	email = request.form.get('email')
	errors = []
	if password1 != password2:
		errors.append('Passwords do not match.')
	email_parts = parseaddr(email)
	if len(email_parts) != 2 or not email_parts[1]:
		errors.append('Invalid email address: ' + str(email))
	user = data.User(username, email)
	if errors:
		# return show_page('/signup.html', 'Sign Up', errors=errors)
		pass
	else:
		passwordhash = data.get_password_hash(password1)
		data.save_new_user(user, passwordhash)
		session['user'] = user.username
		return redirect('/editprofile.html')


# TODO: Redirect to the signup page if the user is not signed in.
# TODO: Fill in each text area with what the user already has so the information is not wiped each time.
@app.route('/updateprofile', methods=['POST'])
def update_profile():
	firstname = request.form.get('firstname')
	lastname = request.form.get('lastname')
	age = request.form.get('age')
	gender = request.form.get('gender')
	about = request.form.get('about')
	bio = request.form.get('bio')
	username = session['user']
	data.save_user_profile(username=username, firstname=firstname, lastname=lastname, age=age, gender=gender, about=about, bio=bio)
	return redirect('/profile/{}'.format(username))


# TODO: Remove this later
# @app.route('/testaddlikedusers/<username>')
# def testaddlikedusers(username):
# 	data.test_add_liked_users(username)
# 	return data.test_return_liked_users(username)


# TODO: Remove the like/unlike button from the user's own profile
@app.route('/likeuser/<other_username>')
def like_user(other_username):
	username = session['user']
	data.like_user(username, other_username)
	return "success", 200


@app.route('/unlikeuser/<other_username>')
def unlike_user(other_username):
	username = session['user']
	data.unlike_user(username, other_username)
	return "success", 200
