from flask import request, redirect
from flask_app import app
from flask_app.models.message import Message

@app.route('/messages/new',methods=['POST'])
def new_message():
    ride_id = request.form["ride_id"]
    is_valid = Message.validate_message(request.form)
    if not is_valid:
        return redirect(f"/rides/{ride_id}")
    Message.save(request.form)
    return redirect(f"/rides/{ride_id}")
