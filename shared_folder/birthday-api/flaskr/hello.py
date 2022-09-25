from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

usersInfo = {"Jiahao": "1998-09-21", "diana": "1996-02-10", "cudi": "2021-09-25"}

class HelloUser(Resource):
    def get(self, username):
        # get the birthday of the user and the current day
        user_birthday = usersInfo[username]
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

        print(next_birthday_dt)
        print(today)
        # get days until next birthday
        days_until_bd = (next_birthday_dt - today).days

        if days_until_bd > 0:
            return {"message": "Hello, " + username + "! Your birthday is in " + str(days_until_bd) + " day(s)"}, 200
        else:
            return {"message": "Hello, " + username + "! Happy birthday!"}, 200

    def put(self, username):

        user_birthday = request.form['dateOfBirth']

        # check that the dateOfBirth follows the format
        birthday_dt = datetime.strptime(user_birthday, "%Y-%m-%d")

        usersInfo[username] = request.form['dateOfBirth']

        return '', 204

api.add_resource(HelloUser, '/hello/<string:username>')

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')