# Importing main flask modules for API calls
from flask import Flask, jsonify, request

# dateandtime library for timestamp, pytz to get EST timezone, fmt to specify time format for database insertion
from datetime import datetime
from pytz import timezone
EST = timezone('EST')
fmt = '%Y-%m-%d %H:%M:%S'

# Library to generate randomized token strings for API Keys
import secrets

# Wraps module to create authenticating decorator
from functools import wraps

# OS library to access environment variables
import os

# Importing Flask-Markdown library to render our README on the homepage
from markdown import markdown

# Initializing our main application instance
app = Flask(__name__) 

# Setting SQLAlchemy variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importing our database models (tables) and schema
from models import Record, single_record_schema, multiple_records_schema, AuthenticationKey, db, ma

'''
The function "require_authentication" is a decorator function that requires users to add an authentication key to add, modify or delete record entries.
It will cross-check generated API keys in the "authentication_key" table first.
If there is a match = Allow the action.
If there is no match = Return an error message.
'''
def require_authentication(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        # Return the first API key match from the authentication_keys database
        find_api_key = AuthenticationKey.query.filter_by(key = request.headers.get('api-key')).first()

        # If there is an API key match, go ahead with the function
        if find_api_key is not None:
            return view_function(*args, **kwargs)
        
        # If no match, show an error message
        result = {
            'status': "failed",
            'message': "You are not authenticated! Please add an authentication key to the header and try again!"
        }
        return result
    return decorated_function

'''
This function renders the homepage.
'''
@app.route('/')
def index():
    readme = open("README.md", "r")
    render_readme = markdown(readme.read())

    return render_readme

'''
This functions handles errors if there is no username specified after /generate_key/.
'''
@app.route('/api/generate_key/', methods = ["POST"])
def show_generator_error():
    # Failed Message
    result = {
        'status': "failed",
        'message': "Oops! You forgot to add a username after! Please specify a username and try again!"
    }
    return result

'''
This function generates an API key for a new user. The user can proceed to enter their name in the URL. If the username exists, it will return an error message.
If the username is new, it will proceed by returning the api_key (to be put as a cURL header) alongside with other information. This information is appended to
the authentication_keys table.
'''
@app.route('/api/generate_key/<username>', methods = ["POST"])
def generate_key(username):

    existing_username = AuthenticationKey.query.filter_by(username = username).first()

    if existing_username is None:
        key = secrets.token_urlsafe(16)
        created_on = datetime.now(EST).strftime(fmt) + ' EST'

        new_authentication_key = AuthenticationKey(username, key, created_on)

        db.session.add(new_authentication_key)
        db.session.commit()

        result = {
            'status': "success",
            'username': username,
            'api_key': key,
            'created_on': created_on,
            'message': "Congrats! Your API Key has been created!"
        }
        return result

    result = {
        'status': "failed",
        'message': "The username you are trying to register has been already used!"
    }
    return result
'''
This function will return all the record entries in the record table/any entries added by the API.
'''
@app.route('/api/list', methods = ["GET"])
def show_all_records():
    all_records = Record.query.all()
    return jsonify(multiple_records_schema.dump(all_records))

'''
This function allows users to create a new record, provided they have added an API key to the header. The user can add a timestamp, value1, value2,
value3 (everything is optional) while the id, creationdate, and lastmodificationdate is automatically appended to the entry. It utilizes a try/except block
to get a value, if there is no value, it appends a NULL value to the database.
'''
@app.route('/api/create', methods = ["POST"])
@require_authentication
def add_new_record():
    try:
        timestamp = request.json['timestamp']
    except KeyError:
        timestamp = None

    try:
        value1 = request.json['value1']
    except KeyError:
        value1 = None

    try:
        value2 = request.json['value2']
    except KeyError:
        value2 = None
    
    try:
        value3 = request.json['value3']
    except KeyError:
        value3 = None

    # Logic to check if atleast one field is populated. If everything is empty, it returns an error.
    if (timestamp is None and value1 is None and value2 is None and value3 is None) == True:
        result = {
            'status': "failed",
            'message': "Please populate atleast one field into the record and try again!"
        }
        return result

    # Get current time in UNIX time, and append it to creationdate and lastmodificationdate
    current_time = round(datetime.now().timestamp() * 1000)

    # Adding current time information both creationdate and lastmodificationdate
    creationdate = current_time
    lastmodificationdate = current_time

    # Querying the database to match the api-key to the username
    lastmodifiedby = AuthenticationKey.query.filter_by(key = request.headers.get('api-key')).first().username

    # Append record data to Record class structure
    new_record = Record(timestamp, value1, value2, value3, creationdate, lastmodificationdate, lastmodifiedby)

    # Add it and then commit it
    db.session.add(new_record)
    db.session.commit()

    # Success Message
    result = {
        'status': "success",
        'message': "Your entry has successfully been added to the database!",
        'record_info': single_record_schema.dumps(new_record)
    }

    return result

'''
This function catches exceptions caused by not adding a number after the "read" API Endpoint.
'''
@app.route('/api/read/', methods = ["GET"])
def show_read_error():
    # Failed Message
    result = {
        'status': "failed",
        'message': "Oops! You forgot to add a number after! Please specify a number and try again!"
    }
    return result

'''
This function reads the record ID from the URL and then gets the entry from the database, provided the user has authenticated. If not, it throws an error.
If they have authenticated, it will proceed to show the information.
'''
@app.route('/api/read/<record_id>', methods = ["GET"])
def read_particular_record(record_id):
    particular_record = Record.query.filter_by(id = record_id).first()

    # If record does not exist, throw an error
    if particular_record is None:
        result = {
            'status': "failed",
            'message': "The record does not exist! Please try a different record number!"
        }
        return result

    particular_record_data = single_record_schema.dumps(particular_record)

    result = {
        'status': "success",
        'message': "Record found!",
        'record_info': particular_record_data
    }

    return result

'''
This function catches exceptions caused by not adding a number after the "modify" API Endpoint.
'''
@app.route('/api/modify/', methods = ["PATCH"])
def show_modify_error():
    # Failed Message
    result = {
        'status': "failed",
        'message': "Oops! You forgot to add a number after! Please specify a number and try again!"
    }
    return result

'''
This function allows the users to modify a record, provided they have authenticated with an API key. It searches for a record, if it does not exist,
it throws an error message. Otherwise, it will utilize try/except blocks to further get modified information.
'''
@app.route('/api/modify/<record_id>', methods = ["PATCH"])
@require_authentication
def modify_a_record(record_id):
    # Check if the URL number matches a record ID number
    particular_record = Record.query.filter_by(id = record_id).first()

    # If there is no record, throw an error (Failed Message)
    if particular_record is None:
        result = {
        'status': "failed",
        'message': "The record does not exist! Please try a different record number!"
        }
        return result

    
    #  If there is a record ID with that number, use try/except blocks to give the user options to modify some/all fields, if user makes no changes -
    # then do nothing and keep everything the same.
    
    try:
        new_timestamp = request.json['timestamp']
        particular_record.timestamp = new_timestamp
    except KeyError:
        pass

    try:
        new_value1 = request.json['value1']
        particular_record.value1 = new_value1
    except KeyError:
        pass

    try:
        new_value2 = request.json['value2']
        particular_record.value2 = new_value2
    except KeyError:
        pass
    
    try:
        new_value3 = request.json['value3']
        particular_record.value3 = new_value3
    except KeyError:
        pass

    # Get current rounded UNIX time in milliseconds
    current_time = round(datetime.now().timestamp() * 1000)
    newmodificationdate = current_time

    # Appending new modification date to the record
    particular_record.lastmodificationdate = newmodificationdate

    # Getting the latest modifying person's username by matching their API key to their username from our authenticationkey database.
    latest_username_to_modify = AuthenticationKey.query.filter_by(key = request.headers.get('api-key')).first().username

    # Overriding the lastmodifiedby entry to the new username
    particular_record.lastmodifiedby = latest_username_to_modify

    # Committing the information to the database session.
    db.session.commit()

    # Success Message
    result = {
        'status': "success",
        'message': "Your record has successfully been modified!",
        'record_info': single_record_schema.dumps(particular_record)
    }

    return result

'''
This function catches exceptions caused by not adding a number after the "remove" API Endpoint.
'''
@app.route('/api/remove/', methods = ["DELETE"])
def show_delete_error():
    # Failed Message
    result = {
        'status': "failed",
        'message': "Oops! You forgot to add a number after! Please specify a number and try again!"
    }
    return result

'''
This function finds the record entry by extracting the number from the URL. If the record ID does not exist, it throws an error. Otherwise, it deletes the
record and commits the changes to the database session.
'''
@app.route('/api/remove/<record_id>', methods = ["DELETE"])
@require_authentication
def delete_a_record(record_id):
    # Check if the URL number matches a record ID number
    particular_record = Record.query.filter_by(id = record_id).first()

    # If there is no record, throw an error (Failed Message)
    if particular_record is None:
        result = {
        'status': "failed",
        'message': "The record does not exist! Please try a different record number!"
        }
        return result

    # Delete the record from the database session
    db.session.delete(particular_record)

    # Commit the changes
    db.session.commit()

    # Success Message
    result = {
        'status': "success",
        'message': "Your record has been removed!"
    }

    return result

if __name__ == "__main__":
    app.run(debug = False)