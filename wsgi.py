import os
import logging
import sys
logging.warn(os.environ["DUMMY"])

from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)

from flask_sqlalchemy import SQLAlchemy, abort, request
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

@app.route('/products/', methods=['GET'])
def read_many_products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def read_one_product(id):
    product = db.session.query(Product).get(id)
    if product is None:
        abort(404)
    return product_schema.jsonify(product), 200

@app.route('/products/', methods=['POST'])
def create_one_product():
    product = Product()
    product.name = "Ajout via API create_one_product"
    db.session.add(product)
    db.session.commit()
    ##########################################################
    #TODO# Comment tester si le commit est OK ?
    # Est-il possible de récupérer le code retour du commit ?
    ##########################################################
    if product is None:
        abort(422)
    return product_schema.jsonify(product), 201

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_one_product(id):
    product = db.session.query(Product).get(id)
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    ##########################################################
    #TODO# Comment tester si le delete est OK ?
    # Est-il possible de récupérer le code retour du commit ?
    ##########################################################
    return '', 204


@app.route('/products/<int:id>', methods=['PATCH'])
def update_one_product(id):
    data = request.get_json()
    # sample data input : { "name": "titi" }
    name = data.get('name')
    if data['name'] is None:
        abort(400)
    product = db.session.query(Product).get(id)
    if product is None:
        abort(404)
    product.name = name
    db.session.commit()
    ##########################################################
    #TODO# Comment tester si le patch est OK ?
    # Est-il possible de récupérer le code retour du commit ?
    ##########################################################
    return '', 204

# Debug dans la log flask
#sys.stderr.write("debut ====")
#sys.stderr.write(data['name'])
#sys.stderr.write("fin ====")
#
