from flask_app import app as application

from flask_app.controllers import users
from flask_app.controllers import rides
from flask_app.controllers import messages

if __name__ == "__main__":
    application.run()