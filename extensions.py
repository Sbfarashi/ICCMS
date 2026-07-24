from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Database
db = SQLAlchemy()

# Password Hashing
bcrypt = Bcrypt()

# Database Migration
migrate = Migrate()