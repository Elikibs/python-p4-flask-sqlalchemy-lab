#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    response_body =  '<h1>Zoo app</h1>'
    response = make_response(response_body, 200)
    return response

# animal searched by ID view
@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    # handling  error
    if not animal:
        response_body = '<h1>404 Error, animal not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    # No error occurring
    response_body = f"""
        <h1>ID: {animal.id}</h1>
        <h1>Name: {animal.name}</h1>
        <h2>Species; {animal.species}</h2>
        <h3>Zookeeper; {animal.zookeeper.name}</h3>
        <h4>Enclosure; {animal.enclosure.environment}</h4>
    """
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    # handling error
    if not zookeeper:
        response_body = '<h1>404 Error, animal not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    # no error occurring
    response_body = f"""
        <h1>ID: {zookeeper.id}</h1>
        <h1>Name: {zookeeper.name}</h1>
        <p>Birthday; {zookeeper.birthday}</p>
    """
    # retrives all animals associated with this particular zookeeper
    animals = [animal for animal in zookeeper.animals]

    if not animals:
        response_body += f'<h2>Has no animals at this time.</h2>'
    else:
        for animal in animals:
            response_body += f'<h2>Animal: {animal.name} of Species; {animal.species}</h2>'
    
    response = make_response(response_body, 200)
    return response


@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    # handling error
    if not enclosure:
        response_body = '<h1>404 Error, enclosure not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    # no error occurring
    response_body = f"""
        <h1>ID: {enclosure.id}</h1>
        <h1>Name: {enclosure.environment}</h1>
        <p>Open to visitors; {enclosure.open_to_visitors}</p>
    """
    # retrives all animals associated with this particular zookeeper
    animals = [animal for animal in enclosure.animals]

    if not animals:
        response_body += f'<h2>Has no animals at this time.</h2>'
    else:
        for animal in animals:
            response_body += f'<h2>Animal; {animal.name}, of Species; {animal.species}</h2>'
    
    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
