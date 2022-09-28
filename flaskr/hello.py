from flask import Flask, request, abort
from flask_restful import Resource, Api
from datetime import datetime, date
import sqlite3

app = Flask(__name__)
api = Api(app)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("../database/birthday.db")
    except sqlite3.error as e:
        print(e)
    return conn

class HelloUser(Resource):
    def get(self, username):
        # get the db connection y cursor
        conn = db_connection()
        cursor = conn.cursor()

        # get the birthday of the user and the current day
        cursor = conn.execute("SELECT birthday FROM birthday WHERE username = :username", {"username": username})
        user_birthday = cursor.fetchone()

        # if the user does not exist in our database we raise a 404 error
        if user_birthday is None:
            return {"message": "Error 404. The user with username: '" + username + "' does not exist"}, 404
        user_birthday = user_birthday[0] 
        today = datetime.now()

        # only keep the year, month and day
        today = datetime.strptime(str(today.year) + "-" + 
                str(today.month) + "-" + str(today.day), "%Y-%m-%d")

        # set the year of the birthday to this year
        birthday_dt = datetime.strptime(user_birthday, "%Y-%m-%d")
        next_birthday_dt = birthday_dt.replace(year=today.year)

        # if the birthday of this year has already been celebrated, set the year to the next year
        if today > next_birthday_dt:
            next_birthday_dt = birthday_dt.replace(year=today.year+1)

        # get days until next birthday
        days_until_bd = (next_birthday_dt - today).days

        if days_until_bd > 0:
            return {"message": "Hello, " + username + "! Your birthday is in " + str(days_until_bd) + " day(s)"}, 200
        else:
            return {"message": "Hello, " + username + "! Happy birthday!"}, 200

    def put(self, username):
        # get the db connection y cursor
        conn = db_connection()
        cursor = conn.cursor()

        # check that the username contains only letters
        if not username.isalpha():
            return {"message": "The username can only contain letters, received: " + username}, 400

        user_birthday = request.form['dateOfBirth']

        # check that the dateOfBirth has the correct format
        try:
            birthday_dt = datetime.strptime(user_birthday, "%Y-%m-%d")
        except:
            return {"message": "The field dateOfBirth expects to receive a correct date with the format %YYYY-%MM-%DD, data received: " + user_birthday}, 400
        
        # check that dateOfBirth was prior to today
        today = datetime.now()
        # only keep the year, month and day
        today_dt = datetime.strptime(str(today.year) + "-" + 
                str(today.month) + "-" + str(today.day), "%Y-%m-%d")
        
        if today_dt < birthday_dt:
            return {"message": "The field dateOfBirth must be before than today (" + date(today.year, today.month, today.day).isoformat() + "), data received: " + user_birthday}, 400

        # insert or update the data
        sql = """INSERT OR REPLACE INTO birthday(username, birthday)
                 VALUES (?,?)"""
        cursor.execute(sql, (username, user_birthday))
        conn.commit()

        return '', 204
    
    # This method has been created to remove the users created by the test, due to lack of time, this method has not been tested
    # as it was out of scope of this project
    def delete(self, username):
        conn = db_connection()
        cursor = conn.cursor()
        sql = """DELETE FROM birthday WHERE username=VALUES(?)"""
        cursor.execute(sql, (username))
        conn.commit()
        return '', 204

api.add_resource(HelloUser, '/hello/<string:username>')

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')