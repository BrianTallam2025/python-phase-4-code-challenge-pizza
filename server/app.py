from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False # For pretty printing JSON responses

# Initialize database and migration
migrate = Migrate(app, db)
db.init_app(app)

# Root route for testing connection
@app.route('/')
def home():
    return '<h1>Welcome to the Pizza Restaurant API!</h1>'

# GET /restaurants
# Returns a list of all restaurants with their id, name, and address.
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    # Serialize the restaurants to the desired format
    restaurants_data = [
        {"id": r.id, "name": r.name, "address": r.address}
        for r in restaurants
    ]
    return make_response(jsonify(restaurants_data), 200)


@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        return make_response(jsonify(restaurant.to_dict(rules=('-restaurant_pizzas.restaurant',))), 200)
    else:
        
        return make_response(jsonify({"error": "Restaurant not found"}), 404)


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        # Return 204 No Content for successful deletion with no response body
        return make_response('', 204)
    else:
        # If restaurant not found, return 404 with error message
        return make_response(jsonify({"error": "Restaurant not found"}), 404)


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    
    pizzas_data = [p.to_dict() for p in pizzas]
    return make_response(jsonify(pizzas_data), 200)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    try:
        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)

        if not restaurant:
            return make_response(jsonify({"errors": ["Restaurant not found"]}), 404)
        if not pizza:
            return make_response(jsonify({"errors": ["Pizza not found"]}), 404)

        # Create a new RestaurantPizza instance
        new_restaurant_pizza = RestaurantPizza(
            price=price,
            restaurant_id=restaurant_id,
            pizza_id=pizza_id
        )

        
        db.session.add(new_restaurant_pizza)
        db.session.commit()

    
        return make_response(jsonify(new_restaurant_pizza.to_dict()), 201) # 201 Created
    except ValueError as e:
        db.session.rollback() 
        return make_response(jsonify({"errors": [str(e)]}), 400) 
    except Exception as e:
        
        db.session.rollback()
        return make_response(jsonify({"errors": ["An unexpected error occurred", str(e)]}), 500) # 500 Internal Server Error

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

if __name__ == '__main__':
    app.run(port=5555, debug=True)