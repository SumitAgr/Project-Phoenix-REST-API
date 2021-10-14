# Using Flask's SQLAlchemy extension for our database needs
from flask_sqlalchemy import SQLAlchemy 

# Flask's Marshmallow extension for an integration layer
from flask_marshmallow import Marshmallow

# Importing our main app variable from app.py
from app import app

# Declaring variables for SQLAlchemy and Marshmallow
db = SQLAlchemy(app) 
ma = Marshmallow(app)

# Creating our "record" table model
class Record(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.Float)
    value1 = db.Column(db.String(255))
    value2 = db.Column(db.Float)
    value3 = db.Column(db.Boolean, unique = False, default = None)
    creationdate = db.Column(db.Float)
    lastmodificationdate = db.Column(db.Float)
    lastmodifiedby = db.Column(db.String(255))
    
    # Initializing all the variables
    def __init__(self, timestamp, value1, value2, value3, creationdate, lastmodificationdate, lastmodifiedby):
        self.timestamp = timestamp
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.creationdate = creationdate
        self.lastmodificationdate = lastmodificationdate
        self.lastmodifiedby = lastmodifiedby

# Declaring the variables to be exposed to the JSON response
class ListAllRecords(ma.Schema):
    class Meta:
        # Exposing the needed fields to the API
        fields = ('id', 'timestamp', 'value1', 'value2', 'value3', 'lastmodifiedby')        

# single_record_schema returns one item, while multiple_record_schema returns multiple items
single_record_schema = ListAllRecords()
multiple_records_schema = ListAllRecords(many = True)

# Creating our API Key table model
class AuthenticationKey(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), nullable = False)
    key = db.Column(db.String(255), nullable = False)
    created_on = db.Column(db.String(255), nullable = False)

    # Initializing the variables
    def __init__(self, username, key, created_on):
        self.username = username
        self.key = key
        self.created_on = created_on