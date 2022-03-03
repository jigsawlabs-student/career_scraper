from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/career_scraper"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


migrate = Migrate()
migrate.init_app(app, db)

from src.models.city import City
from src.models.company import Company
from src.models.position_location import PositionLocation
from src.models.position import Position
from src.models.state import State