<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/WF4UOqj.png" alt="API logo"></a>
</p>

<h3 align="center">Project Phoenix</h3>

<div align="center">

![Language](https://img.shields.io/badge/Python-3.8.7-blue.svg)

</div>

---

<p align="center"> 💻 Presenting Project Phoenix! A RESTful API made with Python and the Flask microframework!
    <br> 
</p>

# 📝 Table of Contents
- [About](#about)
- [How it works](#working)
- [Database](#database)
- [Data types](#datatypes)
- [API Endpoints](#endpoints)
- [Step-by-Step Instructions](#usage)
  - [Authentication](#authentication)
  - [Create a record](#create)
  - [Read all records](#readall)
  - [Read a record](#readone)
  - [Modify a record](#modify)
  - [Remove a record](#remove)
- [pip requirements](#pip)
- [Built Using](#built_using)
- [Authors](#author)
- [Acknowledgment](#acknowledgement)

## ℹ️ About <a name = "about"></a>
I created Project Phoenix to showcase a sample REST API. Made with Python's Flask framework with a Postgres database on the backend. It is hosted on Heroku with a CI/CD pipeline to this GitHub repository.


## 🧐 How it works <a name = "working"></a>

The API is written using Python 3.8.7, it utilizes Flask as a micro-framework for API calls, PostgresDB for database needs and is hosted live on Heroku's free tier.

I think security is of utmost importance. Therefore, I have introduced some features that can enhance the security of an API. Here's how it works:

The API first asks a user to generate an API key. After the key has been generated, the user needs to include the API key as a header to their cURL command/JSON request to authenticate their API POST requests. The table "authenticationkey" cross-checks whether a user has a valid API key and lets them continue their request if it is valid. Without authentication, the user has the ability to check the list of records or a single record.

Although, you may argue that anyone can make an API key and make changes, this feature gives us a blueprint for features in the future where we can collect things like name, email, and phone number to prevent API abuse.

Another feature that I have introduced is "lastmodifiedby". It stores the last user that modified a record by associating their API key to their username, making it easier to track the people who have been making changes.

## 📦 Database <a name = "database"></a>

### Number of tables in the database
The API database has two tables - "<u>record</u>" and "<u>authenticationkey</u>".

- record stores a record's ID, timestamp, value1, value2, value3, creationdate, lastmodificationdate, lastmodifiedby
- authenticationkey stores an API key's ID, username, the value of the key, the date it was created on

### Data that is created by the user:
- In table "record" - timestamp, value1, value2, value3 (atleast any 1 field is required to complete an initial successful POST request)
- In table "authenticationkey" - username (a unique username can be chosen by the user - existing usernames will return an error)

### Data that is created/populated by the API:
- In table "record" - id, creationdate, lastmodificationdate, lastmodifiedby
- In table "authenticationkey" - id, key, created_on

The user has the ability to create, read, modify as well as remove a record - given they are authenticated.

## ✔️ Data types <a name = "datatypes"></a>
|Field                  |Accepted data types|
|--                     |--|
|timestamp | FLOAT |
|value1              | STRING | 
|value2            | FLOAT |
|value3    | BOOLEAN |

## 🖥️ API Endpoints <a name = "endpoints"></a>

|Route                  |Description|
|--                     |--|
|/api/generate_key/:username | Generates an API Key for the specified username|
|/api/list              | Lists all the records|
|/api/create            | Creates a record|
|/api/read/:record_id    | Reads a record|
|/api/modify/:record_id  | Updates a particular record |
|/api/remove/:record_id  | Removes a particular record |

## 🚀 Step-by-Step Instructions <a name = "usage"></a>

Looking to play around with the API? Great! Let's get started.

## <center><b>[GET] AUTHENTICATION</b></center> <a name = "authentication"></a>

- Step 1: Make a GET request to the following URL to get an API key. Make sure to insert your username in place of the parentheses!
```
https://project-phoenix.herokuapp.com/api/generate_key/(INSERT_USERNAME_HERE)

is changed to

https://project-phoenix.herokuapp.com/api/generate_key/sumit
```
- Step 2: Awesome! You should have your own API key ready for use!

Sample JSON success response:
```
{
    "api_key": "1S-37823MlH3stph2uTYvA",
    "created_on": "0000-00-00 00:00:00 EST",
    "message": "Congrats! Your API Key has been created!",
    "status": "success",
    "username": "sumit"
}
```

Sample JSON failed response <i>if there is no username specified</i>:
```
{
    'status': "failed",
    'message': "Oops! You forgot to add a username after! Please specify a username and try again!"
}
```

Sample JSON failed response <i>if the username is taken</i>:
```
{
    'status': "failed",
    'message': "The username you are trying to register has been already used!"
}
```

- Step 3: Note down the API key that is generated - (16 characters long)
```
1S-37823MlH3stph2uTYvA
```

- Step 4: Add the API key with a "api-key" header to your request
```
api-key: 1S-37823MlH3stph2uTYvA
```

- Step 5: Set your Content-Type header to "application/json"

```
Content-Type: application/json
```

- Step 6: Double-check if the header information is correct. <b>For example:</b>

<img width=780x height=150px src="https://i.imgur.com/ORU24Xh.png" alt="header-info"></a>

- Step 7: You are now ready to use the other requests in the API!

‼️<u>NOTE: The following instructions assume that you have already authenticated by inserting the API key to the header!</u>‼️

If there is no authentication key attached to the header, this is the error response you will get:
```
{
    'status': "failed",
    'message': "You are not authenticated! Please add an authentication key to the header and try again!"
}
```


## <center><b>[POST] TO CREATE A RECORD:</b></center> <a name = "create"></a>

- Step 1: Make a POST request and enter your desired information to create a record, for example:

```
{
    "timestamp": 6789998212,
    "value1": "Hello",
    "value2": 2021.01,
    "value3" true
}
```

- Step 2: Remember to populate atleast 1 field (timestamp, value1, value2, value3) for the request to work. Hit Send!

Sample JSON success response:
```
 {
    "message": "Your entry has successfully been added to the database!",
    "record_info": "{"lastmodifiedby": "sumit",
                     "id": 5,
                      "value1": "German Shepherd",
                       "value2": 781230.21,
                        "timestamp": 828283281.21,
                         "value3": true}",
    "status": "success"
}
```

It should work correctly if you have followed the instructions correctly. If it doesn't work, make sure you have:
* Entered the API key correctly
* Added the content type correctly
* Populated atleast one field
* Enclosed fields in double quotations
* Added commas after every field
* Added curly brackets in the start and end
* Sent text is JSON format (some clients throw an error, if not specified)

Sample JSON failed response <i>if no field is populated</i>:
```
{
    'status': "failed",
    'message': "Please populate atleast one field into the record and try again!"
}
```

## <center><b>[GET] TO READ ALL RECORDS:</b></center> <a name = "readall"></a>

- Step 1: Send a GET request to the following URL:

```
https://project-phoenix.herokuapp.com/api/list
```

- Step 2: It should give you a response!

Sample JSON success response:
```
[
    {
        "id": 1,
        "lastmodifiedby": "ironman",
        "timestamp": 2392822832.21,
        "value1": "Boston Terrier",
        "value2": 9938212273.32,
        "value3": true
    },
    {
        "id": 2,
        "lastmodifiedby": "thor",
        "timestamp": 8929109,
        "value1": "The only thing permanent in life is impermanence!",
        "value2": 88239244423.21,
        "value3": false
    },
    {
        "id": 3,
        "lastmodifiedby": "blackwidow",
        "timestamp": 6789998212.0,
        "value1": "What a great day!",
        "value2": 221220231.01,
        "value3": true
    },
    {
        "id": 4,
        "lastmodifiedby": "loki",
        "timestamp": 67182,
        "value1": "Where are the mere mortals?",
        "value2": 88239244423.21,
        "value3": false
    },
    {
        "id": 5,
        "lastmodifiedby": "captain_america",
        "timestamp": 828283281.21,
        "value1": "No, I don't think I will..",
        "value2": 781230.21,
        "value3": true
    }
]
```

## <center><b>[GET] TO READ A PARTICULAR RECORD:</b></center> <a name = "readone"></a>

- Step 1: Decide on the record ID you want to read. Let's take 5 as an example:

```
https://project-phoenix.herokuapp.com/api/read/(ENTER_RECORD_ID_HERE)

is changed to

https://project-phoenix.herokuapp.com/api/read/5
```

- Step 2: Send a GET request to your URL and you should be all set

Sample JSON success response:
```
{
    "message": "Record found!",
    "record_info": "{"value2": 781230.21,
                     "lastmodifiedby": "captain_america",
                      "id": 5,
                       "value1": "No, I don't think I will..",
                        "timestamp": 828283281.21,
                         "value3": true}",
    "status": "success"
}
```

Sample JSON failed response <i>if there is no record number specified</i>:
```
{
    'status': "failed",
    'message': "Oops! You forgot to add a number after! Please specify a number and try again!"
}
```

## <center><b>[PATCH] TO MODIFY A PARTICULAR RECORD:</b></center> <a name = "modify"></a>

- Step 1: Decide on the record ID you want to read. Our example is with number 5.

```
https://project-phoenix.herokuapp.com/api/modify/(ENTER_RECORD_ID_HERE)

is changed to

https://project-phoenix.herokuapp.com/api/modify/5
```

- Step 2: Specify a PATCH request and populate any or all fields (timestamp, value1, value2, value3)

```
{
  "value1": "No, I don't think I will.",
  "value2": 781230.21,
  "value3": true
}

is changed to 

{
  "value1": "Yes I think I won't....",
  "value2": 1920.02,
  "value3": false
}
```

- Step 3: Your data should be modified and it will show a new field - lastmodifiedby. This will be the latest user who modifed this entry.

Sample JSON success response:

```
{
    "message": "Your record has successfully been modified!",
    "record_info": "{"value2": 1920.02,
                     "lastmodifiedby": "falcon",
                      "id": 5,
                       "value1": "Yes I think I won't....",
                        "timestamp": 828283281.21,
                         "value3": false}",
    "status": "success"
}
```

Sample JSON failed response <i>if the record does not exist</i>:
```
{
    'status': "failed",
    'message': "The record does not exist! Please try a different record number!"
}
```

Sample JSON failed response <i>if the record number is not specified</i>:
```
{
    'status': "failed",
    'message': "Oops! You forgot to add a number after! Please specify a number and try again!"
}
```

## <center><b>[DELETE] TO REMOVE A PARTICULAR RECORD:</b></center> <a name = "remove"></a>

- Step 1: Decide on the record you wanna remove. Our example is record no. 5

```
https://project-phoenix.herokuapp.com/api/remove/(ENTER_RECORD_ID_HERE)

is changed to

https://project-phoenix.herokuapp.com/api/remove/5
```

- Step 2: Send a DELETE request to the URL. You should see your record removed.

Sample JSON success response:
```
{
    "message": "Your record has been removed!",
    "status": "success"
}
```

Sample JSON failed response <i>if record number is not specified</i>:
```
{
    'status': "failed",
    'message': "Oops! You forgot to add a number after! Please specify a number and try again!"
}
```

NOTE: A common error is to write "delete" instead of the required "remove" in the URL. Please make sure it is correct if you are encountering an error!

## ⛏️ pip requirements <a name = "pip"></a>
### Python version is 3.8.7
```
aniso8601==8.1.0
click==7.1.2
Flask==1.1.2
Flask-Markdown==0.3
flask-marshmallow==0.14.0
Flask-SQLAlchemy==2.4.4
gunicorn==20.0.4
itsdangerous==1.1.0
Jinja2==2.11.2
Markdown==3.3.3
MarkupSafe==1.1.1
marshmallow==3.10.0
marshmallow-sqlalchemy==0.24.1
psycopg2==2.8.6
pytz==2020.5
six==1.15.0
SQLAlchemy==1.3.22
Werkzeug==1.0.1
```

## ⛏️ Built Using <a name = "built_using"></a>

Python |  Flask  | PostgreSQL | Heroku |
:-----:|:-----:|:-----:|:-----:|
![https://www.python.org/](https://img.icons8.com/dusk/64/000000/python.png)  |  ![https://flask.palletsprojects.com/](https://i.imgur.com/cST5hkz.png) | ![https://www.postgresql.org/](https://img.icons8.com/color/48/000000/postgreesql.png)  | ![https://www.heroku.com](https://img.icons8.com/color/48/000000/heroku.png)


+ Python 3.8.7
+ Flask 1.1.2 (Extensions used: flask-sqlalchemy, flask-marshmallow)
+ PostgreSQL 2.4
+ Heroku Free Dyno


## ✍️ Author <a name = "author"></a>
+ Sumit Agrawal

## 😃 Acknowledgements <a name = "acknowledgement"></a>
+ Thank you for reading!
