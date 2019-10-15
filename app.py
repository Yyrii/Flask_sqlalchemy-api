from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder
from flask_marshmallow import Marshmallow
import requests, json


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Phone_book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)


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


def post_record(data):
    url = "localhost:5000/PhoneBook/"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)


if __name__ == '__main__':
    app.run()
