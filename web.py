#!/usr/bin/env python
import os

from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

DB_FILE = "sqlite3.db"
if os.path.exists(DB_FILE):
    os.unlink(DB_FILE)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(DB_FILE)
db = SQLAlchemy(app)


class Hive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)

    def __init__(self, location="unknown_location"):
        self.location = location


class Bee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    hive_id = db.Column(db.Integer, db.ForeignKey('hive.id'))
    hive = db.relationship('Hive', backref=db.backref('bees', lazy='dynamic'))

    def __init__(self, name, hive):
        self.name = name
        self.hive = hive


# Create the database tables
db.create_all()

manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints
# * /api/hive/:hive_id
# * /api/bee/:bee_id
manager.create_api(Hive)
manager.create_api(Bee)

hive = Hive('backyard')

db.session.add(hive)
for bee_name in ['adam', 'steve']:
    db.session.add(Bee(bee_name, hive))
db.session.commit()


@app.route('/api')
def GET_api():
    routes = []
    for route in app.url_map.iter_rules():
        routes.append(route.rule)
    return jsonify({'data': routes})


if __name__ == '__main__':
    app.run()
