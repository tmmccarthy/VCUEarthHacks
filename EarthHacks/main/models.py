from datetime import datetime
from main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    receipt = db.relationship('Receipt', backref='user', lazy=True)
    
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item = db.relationship('Item', backref='receipt', lazy=True)
    
    def __repr__(self):
        return f"Receipt('{self.store}', '{self.location}', '{self.date}')"
        
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)
    material = db.relationship('Material', backref='item', lazy=True)
    
    def __repr__(self):
        return f"Item('{self.name}')"

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    method = db.relationship('Method', backref='material', lazy=True)
    
    def __repr__(self):
        return f"Material('{self.name}')"

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    
    def __repr__(self):
        return f"Method('{self.description}')"