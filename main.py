from flask import Flask, render_template

app = Flask(__name__)

import route

if __name__ == '__main__':
    app.run()

