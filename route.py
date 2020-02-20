from flask import render_template, request, session, redirect
from email.utils import parseaddr
from main import app
import data

# Part of this code is based on the code found at https://github.com/timothyrjames/cs1520 with permission from the instructor


@app.route('/')
@app.route('/homepage.html')
def root():
	return render_template('homepage.html')


@app.route('/signup.html')
def signup():
	return render_template('signup.html')


@app.route('/signin.html')
def signin():
	return render_template('signin.html')


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

@app.route('/profile/<username>')
def profile_page(username):
	return "Placeholder for {}".format(username)


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
		data.save_user(user, passwordhash)
		session['user'] = user.username
		return redirect('/profile/{}'.format(username))
