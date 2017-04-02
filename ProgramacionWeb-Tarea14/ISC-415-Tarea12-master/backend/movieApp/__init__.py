from flask import abort, Flask, g, render_template, request
from flask_cors import CORS
from movier.main.routes import main
from movier.config import configure_app
from movier.data.models import db

app = Flask(__name__, template_folder='templates')

CORS(app)
configure_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main, url_prefix='/')

