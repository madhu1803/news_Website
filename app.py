"""
I keep app.py very thin.
"""
from flask import Flask
import os.path
from flask_sqlalchemy  import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "madhu"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
Bootstrap(app)
db = SQLAlchemy(app)


# Here I would set up the cache, a task queue, etc.