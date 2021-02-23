from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager

app = Flask(__name__)
# will protect against modifying cookies ,cross site request(CSR ) FORGERRY ATTACKS


app.config['SECRET_KEY']='ca17766457b6d55717ec'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/zaid/Documents/flaskblog/app/web.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from app import routes

