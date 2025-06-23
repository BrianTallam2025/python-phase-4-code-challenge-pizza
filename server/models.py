from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255))
   
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    
    restaurant_pizzas = db.relationship(
        'RestaurantPizza',
        back_populates='restaurant',
        cascade='all, delete-orphan',
        single_parent=True 
    )

    
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    def __repr__(self):
        return f'<Restaurant {self.id}: {self.name}>'

  
    def to_dict(self, rules=('-restaurant_pizzas.restaurant',)):
        result = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
        }
        if 'restaurant_pizzas.restaurant' not in rules:
            result['restaurant_pizzas'] = [rp.to_dict(rules=('-restaurant', '-pizza.restaurant_pizzas',)) for rp in self.restaurant_pizzas]
        return result


class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    def __repr__(self):
        return f'<Pizza {self.id}: {self.name}>'

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
        }


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

   
    @validates('price')
    def validate_price(self, key, price):
        if not isinstance(price, int) or not (1 <= price <= 30):
            raise ValueError("Price must be an integer between 1 and 30")
        return price

    def __repr__(self):
        return f'<RestaurantPizza {self.id}: Price={self.price}, Restaurant_ID={self.restaurant_id}, Pizza_ID={self.pizza_id}>'


    def to_dict(self, rules=()):
        result = {
            "id": self.id,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id": self.pizza_id,
          
        }
        
        if '-restaurant' not in rules:
            
            result['restaurant'] = self.restaurant.to_dict(rules=('-restaurant_pizzas',))
        if '-pizza' not in rules:
            result['pizza'] = self.pizza.to_dict()
        return result

