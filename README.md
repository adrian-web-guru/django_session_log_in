# django_session_memcache
This project is an ENDPOINT to validate if a user has a session in cache or not.

- <code>api/get-session-status/</code> the url will get as parameters ?name=Foo Bar

and will check if session exists and is not expired. will return the response based on the status.
  
Requirements.txt file contains the list of packages used for this project

# To install
pipenv install -r path/requirements.txt


You need to run python manage.py makemigrations -> then migrate to have working DB/ORM

# TO START SERVER
python manage.py runserver PORT


# ENDPOINTS API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GET '' -> DRF landpage

POST create-user/ 
    request: {
        "username": "aaddddd"
    , "password":"1235555"
    }

GET token_endpoint/  (get all users) [name is thou router]

*create a super user with python manage.py createsuperuser

JWT POST api/token/   
    request: {
      "username": "super_user"
    , "password":"1235555"
    }

Once with a token, use it at auth token at requests!

And then log-in to start the session & cache process

POST api/session-status/  
    request: {
      "username": "badilladrian"
    , "password":"123456"
    }
    response:
    {
        "session_information": {
            "id_session": [
                "rqm2qtqwpwdyqeuqdptqdlmqckdmi17k"
            ],
            "created_date": "2021-01-25",
            "username": "juan123",
            "_session_expiry": 120,
            "_session_init_timestamp_": 1611603123.514737
        }
    }

You need to create cache first,
so check not to get this error:
"You have to log in first @WheelsUp a session!"


# SCOPE OF ASSIGMENT 
GET api/session-status/  
    request: {
      "name": "badilladrian"
    }
    response:{
        true   # if is store at cache
    }

Please visit memcached either W10> or Mac OS
-> $ brew install memcached
-> $ memcached -V
-> $ memcached -vv to start/open current cache

To look your processes and kill django server 
ps auxw | grep runserver 
then kill -9 PID 

# TO RUN UNIT TESTS
python manage.py test