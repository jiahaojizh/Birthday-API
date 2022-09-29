import pytest
import sys
import requests
from datetime import datetime, date

# append the path of the parent directory
sys.path.append("..")

from flaskr import hello

TODAY = datetime.now()
TODAY_ISO = date(TODAY.year, TODAY.month, TODAY.day).isoformat()

HOST = "172.17.0.2"
USER = "newuser"

### DB CONNECTION
def test_db_connection():
    conn = hello.db_connection()
    assert conn is not None

### POST METHOD
def test_post_user():
    r = requests.put('http://' + HOST + ':5000/hello/' + USER, data={'dateOfBirth': '1998-01-01'})
    assert r.status_code == 204
    assert r.text == ''
    requests.delete('http://' + HOST + ':5000/hello/' + USER)

def test_post_user_with_invalid_username():
    r = requests.put('http://' + HOST + ':5000/hello/n3w-us4r', data={'dateOfBirth': '1998-01-01'})
    assert r.status_code == 400
    assert r.json()["message"] == "The username can only contain letters, received: n3w-us4r"

def test_post_user_wrong_date():
    r = requests.put('http://' + HOST + ':5000/hello/' + USER, data={'dateOfBirth': '2050-01-01'})
    assert r.status_code == 400
    assert r.json()["message"] == "The field dateOfBirth must be before than today (" + TODAY_ISO + "), data received: 2050-01-01"

def test_post_user_incorrect_date_format():
    r = requests.put('http://' + HOST + ':5000/hello/' + USER, data={'dateOfBirth': '1998-00-00'})
    assert r.status_code == 400
    assert r.json()["message"] == "The field dateOfBirth expects to receive a correct date with the format %YYYY-%MM-%DD, data received: 1998-00-00"

### GET METHOD
def test_get_user():
    # set a day different than the current day
    day = 27
    if day == TODAY.day:
        day = 12
    r = requests.put('http://' + HOST + ':5000/hello/' + USER, data={'dateOfBirth': date(TODAY.year, TODAY.month, day).isoformat()})
    assert r.status_code == 204
    r = requests.get('http://' + HOST + ':5000/hello/' + USER)
    assert r.status_code == 200
    assert "Hello, " + USER + "! Your birthday is in" in r.json()["message"]
    requests.delete('http://' + HOST + ':5000/hello/' + USER)

def test_get_user_with_birthday():
    r = requests.put('http://' + HOST + ':5000/hello/' + USER, data={'dateOfBirth': date(TODAY.year-20, TODAY.month, TODAY.day).isoformat()})
    r = requests.get('http://' + HOST + ':5000/hello/' + USER)
    assert r.status_code == 200
    assert r.json()["message"] == "Hello, " + USER + "! Happy birthday!"
    requests.delete('http://' + HOST + ':5000/hello/' + USER)

def test_get_non_existent_user():
    r = requests.get('http://' + HOST + ':5000/hello/nonexistentuser')
    assert r.status_code == 404
    assert r.json()["message"] == "Error 404. The user with username: 'nonexistentuser' does not exist"

