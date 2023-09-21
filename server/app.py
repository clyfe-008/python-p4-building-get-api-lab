from flask import Flask, jsonify,app,db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
migrate = Migrate(app, db)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
db = SQLAlchemy(app)

class Bakery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class BakedGood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = []
    for bakery in bakeries:
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }
        bakery_list.append(bakery_dict)
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }
        return jsonify(bakery_dict)
    return jsonify({'message': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.all()
    baked_goods_list = []
    for baked_good in baked_goods:
        baked_good_dict = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at
        }
        baked_goods_list.append(baked_good_dict)
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    baked_goods = BakedGood.query.all()
    if baked_goods:
        most_expensive = max(baked_goods, key=lambda x: x.price)
        most_expensive_dict = {
            'id': most_expensive.id,
            'name': most_expensive.name,
            'price': most_expensive.price,
            'created_at': most_expensive.created_at
        }
        return jsonify(most_expensive_dict)
    return jsonify({'message': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run()
