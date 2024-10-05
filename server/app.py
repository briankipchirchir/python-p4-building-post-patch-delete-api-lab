#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries: returns all bakeries as JSON
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_list), 200)

# GET /bakeries/<int:id>: returns a single bakery by id with its baked goods
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return make_response(jsonify(bakery.to_dict(nested=True)), 200)
    return make_response({"error": "Bakery not found"}, 404)

# POST /baked_goods: create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=float(data.get('price')),
        bakery_id=int(data.get('bakery_id'))
    )
    db.session.add(new_baked_good)
    db.session.commit()
    return make_response(jsonify(new_baked_good.to_dict()), 201)

# PATCH /bakeries/<int:id>: update a bakery's details
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        data = request.form
        bakery.name = data.get('name', bakery.name)
        db.session.commit()
        return make_response(jsonify(bakery.to_dict()), 200)
    return make_response({"error": "Bakery not found"}, 404)

# DELETE /baked_goods/<int:id>: delete a baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return make_response({"message": "Baked good deleted"}, 200)
    return make_response({"error": "Baked good not found"}, 404)

# GET /baked_goods/by_price: returns all baked goods sorted by price (desc)
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [good.to_dict() for good in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

# GET /baked_goods/most_expensive: returns the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return make_response(jsonify(most_expensive.to_dict()), 200)
    return make_response({"error": "No baked goods found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
