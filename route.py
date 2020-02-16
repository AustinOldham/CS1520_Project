from main import app

@app.route('/')
def hello_world():
	return "Modular test"

@app.route('/signup')
def signup():
	return "Sign up placeholder"

@app.route('/signin')
def signin():
	return "Sign in placeholder"

@app.route('/profile/<username>')
def profile_page(username):
	return "Placeholder for {}".format(username)
