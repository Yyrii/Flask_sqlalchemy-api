from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg' : 'Hello World!'})


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



@app.route('/PhoneBook',methods=['POST'])
def add_record():
    id = request.json['id']
    name = request.json['name']
    operator = request.json['operator']
    number = request.json['number']

    new_record = PhoneBook(id, name, operator, number)

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"id" : "{}".format(new_record.id),
                    "name": "{}".format(new_record.name),
                    "operator": "{}".format(new_record.operator),
                    "number": "{}".format(new_record.number)})


@app.route('/PhoneBook', methods=['GET'])
def get_record():
    data = PhoneBook.query.all()
    r = request.get(data)
    return jsonify(r)

if __name__ == '__main__':
    app.run()
