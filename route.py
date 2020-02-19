from main import app

@app.route('/')
@app.route('/homepage.html')
def root():
  return render_template('homepage.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
	return "Sign in placeholder"

@app.route('/profile/<username>')
def profile_page(username):
	return "Placeholder for {}".format(username)
