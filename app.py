from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder
from flask_marshmallow import Marshmallow
import requests, json
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)

# ---------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///phone_book.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class PhoneBook2(Base):
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

def init_db2():
    Base.metadata.create_all(bind=engine)


#----------------------------------------------





def init_db():
    db.create_all()

def add_elements():
    db_session.add(PhoneBook2('4', 'Karolina', 'Play', '111222333'))
    db_session.commit()


class PhoneBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    operator = db.Column(db.String(16))
    number = db.Column(db.String(11))

    def __init__(self, id, name, operator, number):
        self.id = id
        self.name = name
        self.operator = operator
        self.number = number


ma = Marshmallow(app)
class DecoderSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "operator", "number")

pb_one_record_schema = DecoderSchema()
pb_records_schema = DecoderSchema(many=True)


# ADD ELEMENT
@app.route('/PhoneBook',methods=['POST'])
def add_record():
    id = request.json['id']
    name = request.json['name']
    operator = request.json['operator']
    number = request.json['number']

    new_record = PhoneBook(id, name, operator, number)

    db.session.add(new_record)
    db.session.commit()

    return pb_one_record_schema.jsonify(new_record)


# ADD MULTIPLE ELEMENTS
@app.route('/PhoneBook',methods=['POST'])
def add_multiple():
    id = "10"
    name = "ewfwe"
    operator = "rg"
    number = "eee"

    new_record = PhoneBook(id, name, operator, number)

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"id" : "{}".format(id),
                    "name" : "{}".format(name),
                    "operator":"{}".format(operator),
                    "number":"{}".format(number)})

# GET ALL ELEMENTS
@app.route('/PhoneBook', methods=['GET'])
def get_all_records():
    all_records = pb_records_schema.dump( PhoneBook.query.all() )
    return jsonify(all_records)


# GET SPECIFIC RECORD
@app.route('/PhoneBook/<id>', methods=['GET'])
def get_record(id):
    record_of_intrest = pb_one_record_schema.dump( PhoneBook.query.get(id) )
    return jsonify(record_of_intrest)


# UPDATE RECORD
@app.route('/PhoneBook/<id>', methods=['PUT'])
def update_record(id):
    record_of_intrest = PhoneBook.query.get(id)

    record_of_intrest.id = request.json['id']
    record_of_intrest.name = request.json['name']
    record_of_intrest.operator = request.json['operator']
    record_of_intrest.number = request.json['number']

    db.session.commit()

    return pb_one_record_schema.jsonify(record_of_intrest)


# DELETE RECORD
@app.route('/PhoneBook/<id>', methods=['DELETE'])
def delete_record(id):
    record_of_intrest = PhoneBook.query.get(id)

    db.session.delete(record_of_intrest)
    db.session.commit()

    return pb_records_schema.jsonify(record_of_intrest)



if __name__ == '__main__':
    app.run()
