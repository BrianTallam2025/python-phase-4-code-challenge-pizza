from app import app
from models import db, Restaurant, Pizza, RestaurantPizza
from datetime import datetime

with app.app_context():
    print("Deleting existing data...")
    # Delete existing data in reverse order of dependency
    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()
    db.session.commit()
    print("Existing data deleted.")

    print("Creating restaurants...")
    r1 = Restaurant(name="Karen's Pizza Shack", address="123 Main St", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    r2 = Restaurant(name="Sanjay's Pizza", address="456 Oak Ave", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    r3 = Restaurant(name="Kiki's Pizza", address="789 Pine Ln", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    r4 = Restaurant(name="The Crusty Corner", address="101 Elm Blvd", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.session.add_all([r1, r2, r3, r4])
    db.session.commit()
    print("Restaurants created.")

    print("Creating pizzas...")
    p1 = Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Mozzarella, Basil", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    p2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Mozzarella, Pepperoni", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    p3 = Pizza(name="Veggie Delight", ingredients="Dough, Tomato Sauce, Mozzarella, Bell Peppers, Onions, Mushrooms", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    p4 = Pizza(name="Hawaiian", ingredients="Dough, Tomato Sauce, Mozzarella, Ham, Pineapple", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    p5 = Pizza(name="BBQ Chicken", ingredients="Dough, BBQ Sauce, Mozzarella, Chicken, Red Onion", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    p6 = Pizza(name="Spicy Sausage", ingredients="Dough, Spicy Tomato Sauce, Mozzarella, Italian Sausage", created_at=datetime.utcnow(), updated_at=datetime.utcnow())

    db.session.add_all([p1, p2, p3, p4, p5, p6])
    db.session.commit()
    print("Pizzas created.")

    print("Creating restaurant_pizzas (associations)...")
    rp1 = RestaurantPizza(restaurant=r1, pizza=p1, price=15, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp2 = RestaurantPizza(restaurant=r1, pizza=p2, price=18, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp3 = RestaurantPizza(restaurant=r2, pizza=p1, price=16, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp4 = RestaurantPizza(restaurant=r2, pizza=p3, price=17, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp5 = RestaurantPizza(restaurant=r3, pizza=p4, price=20, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp6 = RestaurantPizza(restaurant=r3, pizza=p5, price=22, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp7 = RestaurantPizza(restaurant=r4, pizza=p1, price=14, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp8 = RestaurantPizza(restaurant=r4, pizza=p6, price=19, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp9 = RestaurantPizza(restaurant=r1, pizza=p3, price=17, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    rp10 = RestaurantPizza(restaurant=r2, pizza=p5, price=21, created_at=datetime.utcnow(), updated_at=datetime.utcnow())

    db.session.add_all([rp1, rp2, rp3, rp4, rp5, rp6, rp7, rp8, rp9, rp10])
    db.session.commit()
    print("Restaurant-Pizza associations created.")

    print("Seeding complete!")