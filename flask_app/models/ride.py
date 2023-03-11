from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime


class Ride:
    db_name = "ohana_rideshares"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.destination = db_data["destination"]
        self.pick_up_location = db_data["pick_up_location"]
        self.rideshare_date = db_data["rideshare_date"]
        self.details = db_data["details"]
        self.rider_id = db_data["rider_id"]
        self.driver_id = db_data["driver_id"] if db_data["driver_id"] else None
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

        # ------ Pyhon Sorthand If Else ------
        self.rider = db_data["rider"] if db_data["rider"] else None
        self.driver = db_data["driver"] if db_data["driver"] else None

        # if db_data['rider']:
        #     self.rider = db_data['rider']
        # else:
        #     self.rider = None

        # if db_data['driver']:
        #     self.driver = db_data['driver']
        # else:
        #     self.driver = None

    # 1) READ OPERATIONS
    # 1.1) Get All Rides with rider and driver
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM rides LEFT JOIN users AS riders ON riders.id = rides.rider_id LEFT JOIN users AS drivers ON drivers.id = rides.driver_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        rides = []
        for row in results:
            if row["drivers.first_name"]:
                driver = row["drivers.first_name"] + " " + row["drivers.last_name"]
            else:
                driver = None

            data = {
                "id": row["id"],
                "destination": row["destination"],
                "pick_up_location": row["pick_up_location"],
                "rideshare_date": datetime.strptime(row["rideshare_date"], "%Y-%m-%d").date() if row["rideshare_date"] != "" else "",
                "details": row["details"],
                "rider_id": row["rider_id"],
                "driver_id": row["driver_id"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "rider": row["first_name"] + " " + row["last_name"],
                "driver": driver, 
            }
            rides.append(cls(data))

        return rides
    
    # 1.2) Get One Ride with rider and driver
    @classmethod
    def get_one_with_users(cls, data):
        query =  "SELECT * FROM rides LEFT JOIN users AS riders ON riders.id = rides.rider_id LEFT JOIN users AS drivers ON drivers.id = rides.driver_id WHERE rides.id= %(id)s ;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        row = results[0]
        
        if row['drivers.first_name']:
            driver = row['drivers.first_name'] + " " + row['drivers.last_name']
        else:
            driver = None
        
        data_2 = {
            "id" : row["id"],
            "destination" : row['destination'],
            "pick_up_location" : row['pick_up_location'],
            "rideshare_date" : datetime.strptime(row["rideshare_date"], "%Y-%m-%d").date() if row["rideshare_date"] != "" else "",
            "details" : row['details'],
            "rider_id" : row['rider_id'],
            "driver_id" : row['driver_id'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at'],
            "rider" : row['first_name'] + " " + row['last_name'],
            "driver" : driver
        }
           
        ride = cls(data_2)
        return ride

    # 2) CREATE OPERATIONS
    # 2.1) Create Ride
    @classmethod
    def save(cls, data):
        print(data)
        query = "INSERT INTO rides (destination,pick_up_location,rideshare_date,details,rider_id,driver_id,created_at,updated_at)\
              VALUES (%(destination)s,%(pick_up_location)s ,%(rideshare_date)s,%(details)s,%(rider_id)s,NULL,NOW(),NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    # 3) UPDATE OPERATIONS
    # 3.1) Add Driver to Ride
    @classmethod
    def update(cls, data):
        query = "UPDATE rides SET pick_up_location=%(pick_up_location)s, details=%(details)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # 3.2) Add Driver
    @classmethod
    def add_driver(cls, data):
        query = "UPDATE rides SET driver_id=%(driver_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # 3.3) Canel Driver from Ride
    @classmethod
    def cancel_driver(cls, data):
        query = "UPDATE rides SET driver_id=NULL WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # 4) DELETE OPERATIONS
    # 4.1) Delete Ride
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM rides WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

        # 5) VALIDATIOS
    # 5.1) Validate User
    @staticmethod
    def validate_ride(ride,type):
        is_valid = True
        if type == 'new' and len(ride['destination']) < 3:
            is_valid = False
            flash("Destination must be at least 3 characters.","ride")
        if len(ride['pick_up_location']) < 3:
            is_valid = False
            flash("Pick-up location must be at least 3 characters.","ride")
        if type == 'new' and len(ride['rideshare_date']) == 0:
            is_valid = False
            flash("Rideshare date required", "ride")
        if len(ride['details']) < 10:
            is_valid = False
            flash("Details must be at least 10 characters.","ride")
        return is_valid