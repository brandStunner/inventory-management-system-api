
import os
from flask import Flask, jsonify, request, make_response, session, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from urllib.parse import quote_plus
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY", "fallback_dev_key") #session logins

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST =  os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connection URL for the new database
password = quote_plus(DB_PASSWORD)
DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User User detail Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    hashed_password = db.Column(db.String(200), nullable = False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
        

# Inventory Model(table)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(100),nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return (f"<Item {self.name}>")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description
        }

with app.app_context():
    db.create_all()


# HELPER FUNCTION TO ENFORCE LOGIN 
def login_required(func):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in to access this"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # avoid Flask decorator issues
    return wrapper

####################### login Routes ###################################

# register new user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}),400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "registered successfully"
        }), 201


# login registered user 
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session["user_id"] = user.id #needed for login
        return jsonify({
            "message": "login successful"
            }), 201
    else:
        return jsonify({"message": "invalid username or password"}),401
    
########## LOGOUT ROUTE ####################

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    '''This function makes session inactive and allows for logout'''
    session.pop("user_id", None)
    return jsonify({"message": "logged out successfully"}), 200


############### Inventory Routes ################ 
@app.route("/")
def welcome_page():
    return jsonify({"message":"Welcome to the invenoty page!"})

# GET ROUTE, this is where you view all available options
@app.route("/inventory", methods=["GET"])
@login_required
def view_all():
    '''This function allows logged in users to view api endpoint with all items in inventory'''
    try:
        all_items = Inventory.query.all()

        inventory_items = []
        for inventory_item in all_items:
            inventory_items.append({
                 "id": inventory_item.id,   
                 "name": inventory_item.name,
                 "sku": inventory_item.sku,
                 "quantity": inventory_item.quantity,
                 "price": inventory_item.price,
                 "description": inventory_item.description
                }
            )
        return jsonify({
            "message" : "All inventory items",
            "total": len(inventory_items),
            "items": inventory_items
        })

    except Exception as e:
        return jsonify({"Error": "Failed to retrieve inventory", "error": str(e)}), 500 

# THIS ROUTE ALLOWS YOU VIEW INDIVIDUAL ITEMS USING THEIR IDs
@app.route("/inventory/<int:item_id>", methods=["GET"])
@login_required
def get_item(item_id):
    '''This function allows users to view individual item using their id.'''
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"item": item.to_dict()})


# THIS ROUTE IS WHERE ITEMS ARE ADDED TO THE INVENTORY DATABASE 
@app.route("/inventory", methods = ["POST"])
@login_required
def add_item():
    '''This function is responsible for adding a new inventory item through the route 127.0.0.1:5000/inventory
    using the post method
    '''
    try:
        data = request.get_json()
        name = data.get("name")
        sku = data.get("sku")
        quantity = data.get("quantity")
        price = data.get("price")
        description = data.get("description")

        if not name:
            return jsonify({"error": "name is required"}),400

        try:
            quantity = int(data.get("quantity"))
            price = float(data.get("price"))
        except (TypeError, ValueError):
            return jsonify({"error": "quantity must be an integer and price must be a number"}), 400

        new_inventory_item = Inventory(name = name,sku = sku, quantity = quantity, price = price, description = description)

        db.session.add(new_inventory_item)
        db.session.commit()

        inventory_data = {
            "id": new_inventory_item.id,
            "name": new_inventory_item.name,
            "sku": new_inventory_item.sku,
            "quantity": new_inventory_item.quantity,
            "price": new_inventory_item.price,
            "description": new_inventory_item.description
        }

        
        return make_response(jsonify({
        "message": "new inventory added",
        "item": inventory_data
        })), 201
    
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "item already exists"})),409
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({
        "error": "Error inserting new inventory",
        "details": str(e)
    })), 500


#  PUT ROUTE THIS IS WHERE ITEMS ARE UPDATED 
@app.route("/inventory/<int:item_id>", methods = ["PUT"]) 
@login_required
def update_item(item_id):
    '''This function takes id of an inventory and make changes to it, access through the route
        "localhost/inventory/1" eg if item id is 1
    '''
    try:
        item = Inventory.query.get(item_id)
        if not item:
            return jsonify({"error": "No item found"}),400
        
        data = request.get_json()
        if "name" in data:
            item.name = data["name"]

        if "sku" in data:
            item.sku = data["sku"]

        if "quantity" in data:
            try:
                item.quantity = int(data["quantity"])
            except (TypeError, ValueError):
                return jsonify({"error": "this value must be an integer"}), 400
        
        if "price" in data:
            try:
                item.price = float(data["price"])
            except (TypeError, ValueError):
                return jsonify({"error": "this value must be a number"}), 400
        if "description" in data:
            item.description = data["description"]

        db.session.commit()

        return jsonify({
            "message": "item updated successfully",
            "item": item.to_dict()
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "sku must be unique"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "failed to update item",
            "details": str(e)
            
    }), 500
    
#THIS ROUTE DELETES ITEMS
@app.route("/inventory/<int:item_id>", methods = ["DELETE"])
@login_required
def delete_item(item_id):
    '''This function takes the id of item to delete and deletes it through the route "localhost/inventory/1" if id is 1'''
    try:
        item = Inventory.query.get(item_id)
        if not item:
            return jsonify({"error": "item not found"}), 400 
        
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": f"{item.name} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error deleting item",
            "details": str(e)
            }), 500



if __name__ == "__main__":
    app.run(debug=True)