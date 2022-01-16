from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


with open(f"secrets.txt", "r", encoding="utf-8") as secretfile:
    password = secretfile.readline()

app = Flask(__name__, instance_relative_config=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:{password}@localhost/ctflime"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # dumb line to surpress warnings
db = SQLAlchemy(app)
app.secret_key = f"{password}"

# needs these comments to stop pylint from complaining and autopep8 from moving the damn line
# pylint: disable=wrong-import-position
from app import views  # noqa


def create_app(config_name):
    app.config.from_object(f"config.{config_name}")

    return app
