from flask_pymongo import PyMongo
from config import MONGOURI


def init_db(app):
    # Configuracao do MongoDB
    app.config["MONGO_URI"] = MONGOURI
    mongo = PyMongo(app)
    return mongo
