import pytest
import sys
import requests
from datetime import datetime
from freezegun import freeze_time

# append the path of the parent directory
sys.path.append("..")

from flaskr import hello

### DB CONNECTION
def test_db_connection():
    conn = hello.db_connection()
    assert conn is not None

### POST METHOD
def test_post_user():
    r = requests.put('http://localhost:5000/hello/new-user', data={'dateOfBirth': '1998-01-01'})
    assert r.status_code == 204
    assert r.text == ''

def test_post_user_with_invalid_username():
    r = requests.put('http://localhost:5000/hello/n3w-us4r', data={'dateOfBirth': '1998-01-01'})
    assert r.status_code == 400
    assert r.json()["message"] == "The username can only contain letters, received n3w-us4r"

@freeze_time("2022-09-26")
def test_post_user_wrong_date():
    r = requests.put('http://localhost:5000/hello/new-user', data={'dateOfBirth': '2050-01-01'})
    assert r.status_code == 400
    assert r.json()["message"] == "The field dateOfBirth must be before than today (2022-09-26), data received: 2050-01-01"

def test_post_user_incorrect_date_format():
    r = requests.put('http://localhost:5000/hello/new-user', data={'dateOfBirth': '1998-00-00'})
    assert r.status_code == 400
    assert r.json()["message"] == "The field dateOfBirth expects to receive a correct date with the format %YYYY-%MM-%DD, data received: 1998-00-00"

### GET METHOD
@freeze_time("2022-09-26")
def test_get_user():
    r = requests.put('http://localhost:5000/hello/new-user', data={'dateOfBirth': '1998-09-28'})
    r = requests.get("http://localhost:5000/hello/new-user")
    assert r.status_code == 200
    assert r.json()["message"] == "Hello, new-user! Your birthday is in 2 day(s)"

@freeze_time("2022-09-26")
def test_get_user_with_birthday():
    r = requests.put('http://localhost:5000/hello/new-user', data={'dateOfBirth': '1998-09-26'})
    r = requests.get("http://localhost:5000/hello/new-user")
    assert r.status_code == 200
    assert r.json()["message"] == "Hello, new-user! Happy birthday!"

def test_get_non_existent_user():
    r = requests.get("http://localhost:5000/hello/non-existent-user")
    assert r.status_code == 404
    assert r.json()["message"] == "Error 404. The user with username: 'non-existent-user' does not exist"

