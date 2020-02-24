from flask import Flask

app = Flask(__name__)
app.secret_key = b'fowefhufuhwef87hf2bfsdbuybcquy153Ejs9zxdsqfhk'

import route

if __name__ == '__main__':
    app.run()
