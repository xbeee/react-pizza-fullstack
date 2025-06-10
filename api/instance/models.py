import sys
sys.path.append('../')

from core import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    Fsp = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<profiles %r>' % self.id
    
class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageURl = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    types = db.Column(db.String(10), nullable=False)
    sizes = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<profiles %r>' % self.id
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(10), nullable=False)
    product_size = db.Column(db.String(30), nullable=False)
    imageURL = db.Column(db.String(1000), nullable=False)
    
    def __repr__(self):
        return '<profiles %r>' % self.id
    
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.String(500), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(10), nullable=False)
    product_size = db.Column(db.String(30), nullable=False)
    imageURL = db.Column(db.String(1000), nullable=False)
    
    def __repr__(self):
        return '<profiles %r>' % self.id
    
def Role(name):
    user = User.query.filter_by(name=name).first()
    role = 'user'
    if user.role == 'admin':
        role = 'admin'
    return role
