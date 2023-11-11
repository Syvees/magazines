from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Car: # MODEL AFTER CARS TABLE
    DB = "syvees_black_belt_new"
    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.buyer = None
        self.cars_list = []
        self.sold = data["sold"]

    @classmethod # INSERT A CAR -- IN NEW PAGE
    def save_car(cls, data):
        query = """INSERT INTO cars (price, model, make, year, description, user_id) 
        VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s )"""
        results = connectToMySQL(cls.DB).query_db(query, data)

    @classmethod # GET ALL CARS LEFT JOIN - DASHBOARD (ADVANCED)
    def get_all_cars(cls):
        query = """SELECT *, (SELECT COUNT(user_id) FROM purchases WHERE purchases.car_id = cars.id) AS sold FROM cars 
                LEFT JOIN users ON users.id = cars.user_id"""
        results = connectToMySQL(cls.DB).query_db(query)
        cars = []
        for row in results:
            this_car = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            this_car.buyer = user.User(user_data)
            cars.append(this_car)
        return cars
    
    @classmethod # GET ONE CAR (ADVANCED)
    def get_one_car(cls, data):
        query = """SELECT *, (SELECT COUNT(user_id) FROM purchases WHERE purchases.car_id = cars.id) AS sold FROM cars 
                LEFT JOIN users ON users.id = cars.user_id WHERE cars.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        for row in results:
            this_car = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            this_car.buyer = user.User(user_data)
        return this_car
    
    @classmethod # EDIT A CAR
    def update_car (cls,data):
        query = """UPDATE cars
                SET price=%(price)s, model=%(model)s, make=%(make)s, 
                year=%(year)s, description=%(description)s
                WHERE id = %(id)s"""
        result = connectToMySQL(cls.DB).query_db(query, data) 
        return result
    
    @classmethod # DELETE A CAR
    def delete_car (cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data) 
        return result

    @classmethod # INSERT A PURCHASE
    def save_purchase(cls,data):
        query = "INSERT INTO purchases (user_id, car_id) VALUES (%(user_id)s, %(car_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @staticmethod # NEW CAR VALIDATIONS -- IN NEW AND EDIT PAGES
    def validate_add_car(data): 
        is_valid = True
        if data["price"] == "":
            flash("Price cannot be left blank", "add_car")
            is_valid = False
        if data["price"] != "" and float(data["price"]) <= 0:
            flash("Price cannot be less than $0", "add_car")
            is_valid = False
        if data["model"] == "":
            flash("Model cannot be left blank", "add_car")
            is_valid = False
        if data["make"] == "":
            flash("Make cannot be left blank", "add_car")
            is_valid = False
        if data["year"] == "":
            flash("Year cannot be left blank", "add_car")
            is_valid = False
        if data["description"] == "":
            flash("Description cannot be left blank", "add_car")
            is_valid = False
        return is_valid
