from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Message:
    db_name = "ohana_rideshares"

    def __init__(self, db_data):
      self.id = db_data["id"]
      self.message = db_data["message"]
      self.user_id = db_data["user_id"]
      self.ride_id = db_data["ride_id"]
      self.created_at = db_data["created_at"]
      self.updated_at = db_data["updated_at"]

      # ------ Pyhon Sorthand If Else ------
      self.user = db_data["user"] if db_data["user"] else None

      # if db_data['user']:
      #     self.user = db_data['user']
      # else:
      #     self.user = None

    # 1) READ OPERATIONS

    # 1.1) Get All Rides with rider and driver
    @classmethod
    def get_all(cls, data):
      query = "SELECT * FROM messages LEFT JOIN users ON users.id = messages.user_id LEFT JOIN rides ON rides.id = messages.ride_id WHERE rides.id=%(id)s;"
      results = connectToMySQL(cls.db_name).query_db(query, data)
      messages = []
      for row in results:
          data = {
              "id": row["id"],
              "message": row["message"],
              "user_id": row["user_id"],
              "ride_id": row["ride_id"],
              "created_at": row["created_at"],
              "updated_at": row["updated_at"],
              "user": row["first_name"] + " " + row["last_name"],
          }
          messages.append(cls(data))
      return messages

    # 2) CREATE OPERATIONS
    # 2.1) Create Message
    @classmethod
    def save(cls, data):
      query = "INSERT INTO messages (message, user_id, ride_id, created_at,updated_at) VALUES (%(message)s,%(user_id)s ,%(ride_id)s,NOW(),NOW());"
      # data is a dictionary that will be passed into the save method from server.py
      results = connectToMySQL(cls.db_name).query_db(query, data)
      return results

    # 3) UPDATE OPERATIONS
    # -----

    # 4) DELETE OPERATIONS
    # -----

    # 5) VALIDATIOS
    # 5.1) Validate User
    @staticmethod
    def validate_message(message):
      is_valid = True
      if len(message["message"]) < 1:
          is_valid = False
          flash("Message cannot be empty.", "message")
      return is_valid
