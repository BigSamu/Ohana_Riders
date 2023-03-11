from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.ride import Ride
from flask_app.models.message import Message


@app.route("/rides/dashboard")
def rides_dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    rider = User.get_one(data)
    rides = Ride.get_all()

    # rides_without_driver = [r for r in rides if r.driver == None]
    # rides_with_driver = [r for r in rides if r.driver != None]

    rides_without_driver = []
    rides_with_driver = []
    for r in rides:
        if(r.driver == None):
            rides_without_driver.append(r)
        else:
            rides_with_driver.append(r)

    # users = User.get_all()
    return render_template("dashboard.html",rider=rider, rides_without_driver=rides_without_driver, rides_with_driver=rides_with_driver)


@app.route("/rides/new", methods=["GET", "POST"])
def new_ride():
    # POST REQUEST
    if request.method == "POST":
        is_valid = Ride.validate_ride(request.form, "new")
        if not is_valid:
            return redirect("/rides/new")
        Ride.save(request.form)
        return redirect("/rides/dashboard")

    # GET REQUEST
    if "user_id" not in session:
        return redirect("/")
    return render_template("new_ride.html")

@app.route('/rides/<int:ride_id>/edit', methods=['GET','POST'])
def edit_ride(ride_id):
    # POST REQUEST 
    if request.method == 'POST':
        if not Ride.validate_ride(request.form, "edit"):
            return redirect(f"/rides/{ride_id}/edit")
        Ride.update(request.form)
        return redirect(f"/rides/{ride_id}")
    
    # GET REQUEST
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': ride_id
    }
    ride = Ride.get_one_with_users(data)
    return render_template("edit_ride.html", ride=ride)

@app.route('/rides/<int:ride_id>')
def details_ride(ride_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": ride_id
    }
    ride = Ride.get_one_with_users(data)
    messages = Message.get_all(data)
    return render_template("details_ride.html", ride=ride, messages=messages)


@app.route("/rides/<int:ride_id>/add_driver/<int:driver_id>")
def add_driver(ride_id, driver_id):
    data = {"id": ride_id, "driver_id": driver_id}
    Ride.add_driver(data)
    return redirect("/rides/dashboard")

@app.route('/rides/<int:ride_id>/cancel_driver')
def cancel_driver(ride_id):
    data = {
        'id': ride_id
    }
    Ride.cancel_driver(data)
    return redirect('/rides/dashboard')

@app.route("/rides/<int:ride_id>/delete")
def delete_ride(ride_id):
    data = {
        "id": ride_id,
    }
    Ride.destroy(data)
    return redirect("/rides/dashboard")
