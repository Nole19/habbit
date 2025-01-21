from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Load configuration settings from config.py
app.config.from_object("config.Config")

# Import routes to register them with the app
from app import routes
