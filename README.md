## Flask_sqlalchemy-api is a single api, that allow for basic CRUD (REST) actions using json data.
It also works offline


# Getting started
First things first. What you want to do, after clonning repo to your computer is to setup virtual enviroment
in command window go to the directory, where you have cloned the repo. Type and run:<br/>
$ pipenv shell

### From now on, all the unneccessary addition packages you can install here. So install the following packages. In the command window run:

$ pip intall flask<br/>
$ pip install sqlalchemy<br/>
$ pip install flask-sqlalchemy<br/>
$ pip install -U marshmallow-sqlalchemy<br/>

### Next thing to do is to create new database. In the command window run:
$ python<br/>
```python
from app import init_db
init_db()
```
### Now you can add few records to the database:
```python
from app imort add_few_records
add_few_records()

exit()
```

### Now you are all set, let's run the app
$ python app.py
#### If everthing worked, you should have your server ran

# Operations
You can always call functions offline (those that end with '_'). Or use some additional tool for crud operations. 
Then you will be able, to run server,and test. I have used [Postman](https://www.getpostman.com/). If you want to ADD any data
remember that it is a json-application
```python
headers = {'content-type': 'application/json'}
```

Be aware to enter proper url, otherwise you'll get error.

