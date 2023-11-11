from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.car import Car
from flask_app.models.user import User
from flask_bcrypt import Bcrypt 
from flask import flash

@app.route("/dashboard") # GO TO DASHBOARD
def display_dashboard():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        "id" : session["logged_in_id"]
    }
    one_user = User.get_one_by_id(data)
    all_cars = Car.get_all_cars()
    return render_template("dashboard.html", one_user=one_user, all_cars=all_cars)

@app.route("/new") # RENDER BLANK CAR FORM
def display_car_form():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        "id" : session["logged_in_id"]
    }
    one_user = User.get_one_by_id(data)
    return render_template("new_car.html", one_user=one_user)

@app.route("/add/car", methods=["POST"]) # ADD CAR AND POST
def add_car():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    if not Car.validate_add_car(request.form): # VALIDATION AND RETURN TO ADD TREE FORM
        return redirect("/new")
    data = {
            "price" : request.form["price"],
            "model" : request.form["model"],
            "make" : request.form["make"],
            "year" : request.form["year"],
            "description" : request.form["description"],
            "user_id" : session["logged_in_id"]
        }
    print(data)
    Car.save_car(data)
    return redirect("/dashboard")

@app.route("/edit/<int:car_id>") # RENDER EDIT CARS PRE-POPULATED
def edit_car(car_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        'id':car_id  
    }
    one_car = Car.get_one_car(data)
    one_user = User.get_one_by_id(data)
    id = session["logged_in_id"]
    return render_template("edit.html", one_car=one_car, one_user=one_user, id=id)

@app.route("/update/<int:car_id>", methods=["POST"]) # UPDATE THE RECIPE AND POST
def update_car(car_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    id = car_id
    if not Car.validate_add_car(request.form): # VALIDATION AND RETURN TO ADD TREE FORM
        return redirect(f"/edit/{id}")
    data = {
            "price" : request.form["price"],
            "model" : request.form["model"],
            "make" : request.form["make"],
            "year" : request.form["year"],
            "description" : request.form["description"],
            "id" : id
        }
    Car.update_car(data)
    return redirect("/dashboard")

@app.route("/delete/<int:car_id>") # DELETE A CAR
def delete_recipe(car_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        'id':car_id  
    }
    Car.delete_car(data)
    return redirect("/dashboard")

@app.route("/show/<int:car_id>") # VIEW EACH CAR
def display_car(car_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        'id':car_id  
    }
    one_car = Car.get_one_car(data)
    one_user = User.get_one_by_id(data)
    id = session["logged_in_id"]
    return render_template("show.html", one_car=one_car, one_user=one_user, id=id)

@app.route("/purchase/<int:car_id>") # ADD TREE VISIT
def save_purchase (car_id):
    id = car_id
    data = {
        "user_id" : session["logged_in_id"],
        "car_id" : id
    }
    car_id=id
    Car.save_purchase(data)
    return redirect("/dashboard")

@app.route("/user/<int:user_id>") # SHOW ACCOUNT
def display_account(user_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        "id" : session["logged_in_id"]
    }
    one_account = User.get_user_purchases(data)
    return render_template("account.html", one_account=one_account)