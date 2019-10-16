from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# Flask app initialization and configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_book.sqlite'   # create URI connection to db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                    # gets rid of warning



# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
engine = create_engine('sqlite:///phone_book.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


"""
example Model
if you want to add another one, remember to add element __tablename__
"""
class PhoneBook(Base):
    __tablename__ = 'PhoneBook'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    operator = Column(String(16))
    number = Column(String(11))

    def __init__(self, id, name, operator, number):
        self.id = id
        self.name = name
        self.operator = operator
        self.number = number


# Function used for initialization of a new database
def init_db():
    Base.metadata.create_all(bind=engine)


# function used for adding few elements to just created database
def add_few_records():
    db_session.add(PhoneBook(0, 'Karolina', 'Play', '111222333'))
    db_session.add(PhoneBook(1, 'Michał', 'Play', '555333111'))
    db_session.add(PhoneBook(2, 'Karolina', 'Orange', '000999888'))
    db_session.add(PhoneBook(3, 'Wiktoria', 'T-Mobile', '234223322'))
    db_session.commit()


"""
Function adds new element to the database. New element (rec) has to be PhoneBook, unless you created new model.
usage:
new_record = PhoneBook('4', 'Kacper', 'Orange', '444444213')
add_record(new_record)
"""
def add_record_(rec):
    db_session.add(rec)
    db_session.commit()


def remove_record_(id):
    record_of_intrest = PhoneBook.query.get(id)
    db_session.delete(record_of_intrest)
    db_session.commit()


def get_record_(id):
    record_of_intrest = pb_one_record_schema.dump(PhoneBook.query.get(id))
    return record_of_intrest

#TODO:
def update_record_(id, **kwargs):
    record_of_intrest = pb_one_record_schema.dump(PhoneBook.query.get(id))
    for el in kwargs.items():
        record_of_intrest[el[0]] = str(el[1])
    db_session.commit()


# https://flask-marshmallow.readthedocs.io/en/latest/
ma = Marshmallow(app)
class DecoderSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "operator", "number")

pb_one_record_schema = DecoderSchema()
pb_records_schema = DecoderSchema(many=True)


"""
the following functions requires some addition outside tool.
During tests i was using "Postman".
Be aware that you have to enter proper endpoint. For every funtion you can find it in the decorator (@app.route)
"""
# ADD ELEMENT
@app.route('/PhoneBook', methods=['POST'])
def add_record():
    id = request.json['id']
    name = request.json['name']
    operator = request.json['operator']
    number = request.json['number']

    new_record = PhoneBook(id, name, operator, number)

    db_session.add(new_record)
    db_session.commit()
    return pb_one_record_schema.jsonify(new_record)


# GET ALL ELEMENTS
@app.route('/PhoneBook', methods=['GET'])
def get_all_records():
    all_records = pb_records_schema.dump(PhoneBook.query.all())
    return jsonify(all_records)


# GET SPECIFIC RECORD
@app.route('/PhoneBook/<id>', methods=['GET'])
def get_record(id):
    record_of_intrest = pb_one_record_schema.dump(PhoneBook.query.get(id))
    return jsonify(record_of_intrest)


# UPDATE RECORD
@app.route('/PhoneBook/<id>', methods=['PUT'])
def update_record(id):
    record_of_intrest = PhoneBook.query.get(id)

    record_of_intrest.id = request.json['id']
    record_of_intrest.name = request.json['name']
    record_of_intrest.operator = request.json['operator']
    record_of_intrest.number = request.json['number']

    db_session.commit()
    return pb_one_record_schema.jsonify(record_of_intrest)


# DELETE RECORD
@app.route('/PhoneBook/<id>', methods=['DELETE'])
def delete_record(id):
    record_of_intrest = PhoneBook.query.get(id)

    db_session.delete(record_of_intrest)
    db_session.commit()
    return pb_records_schema.jsonify(record_of_intrest)



if __name__ == '__main__':
    app.run()
