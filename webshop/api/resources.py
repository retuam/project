from flask_restful import Resource
from ..db.models import *
from flask import request, jsonify
import json
from ..api import schemas
from marshmallow import ValidationError


class CategoryResource(Resource):
    def get(self, id=None):
        if id:
            json_obj = schemas.CategorySchema().dumps(Category.objects(id=id).first())
        else:
            json_obj = schemas.CategorySchema(many=True).dumps(Category.get_root_categories().all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = schemas.CategorySchema().loads(json_data)
            Category.objects.create(**res)
            res = json.loads(schemas.CategorySchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = schemas.CategorySchema().loads(json_data)
            Category.objects(id=id).update(**res)
            data = Category.objects(id=id).first()
            json_obj = schemas.CategorySchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Category.objects(id=id).delete()
        return jsonify(data)


class SubcategoryResource(Resource):
    def get(self, id=None):
        if id:
            json_obj = schemas.CategorySchema().dumps(Category.objects(id=id).first())
        else:
            json_obj = schemas.CategorySchema(many=True).dumps(Category.objects.get_child_categories().all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = schemas.SubcategorySchema().loads(json_data)
            Category.objects.create(**res)
            res = json.loads(schemas.SubcategorySchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = schemas.SubcategorySchema().loads(json_data)
            Category.objects(id=id).update(**res)
            data = Category.objects(id=id).first()
            json_obj = schemas.SubcategorySchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Category.objects(id=id).delete()
        return jsonify(data)


class ProductResource(Resource):
    def get(self, id=None, category_id=None, subcategory_id=None):
        if id:
            post = Products.objects(id=id).first()
            post.add_view()
            json_obj = schemas.ProductSchema().dumps(post)
        else:
            if category_id:
                _category = Category.objects(id=category_id).first()
                data = Products.objects.filter(category=_category).all()
            elif subcategory_id:
                _subcategory = Category.objects(id=subcategory_id).first()
                data = Products.objects.filter(subcategory=_subcategory).all()
            else:
                data = Products.objects.all()

            json_obj = schemas.ProductSchema(many=True).dumps(data)

        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = request.get_json(force=True)
        try:
            res = self.edit(json_data)
            Products.objects.create(**res)
            res = json.loads(schemas.ProductSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = request.get_json(force=True)
        try:
            res = self.edit(json_data)
            Products.objects(id=id).update(**res)
            data = Products.objects(id=id).first()
            json_obj = schemas.ProductSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Products.objects(id=id).delete()
        return jsonify(data)

    def edit(self, json_data):
        res = schemas.ProductSchema().loads(json.dumps(json_data))
        res['subcategory'] = Category.objects.filter(name=json_data['subcategory']['title']).first()
        return res


class CartResource(Resource):
    def get(self, id=None):
        if id:
            json_obj = schemas.CartSchema().dumps(Cart.objects(id=id).first())
        else:
            json_obj = schemas.CartSchema(many=True).dumps(Cart.objects.all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = schemas.CartSchema().loads(json_data)
            Cart.objects.create(**res)
            res = json.loads(schemas.CartSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = schemas.CartSchema().loads(json_data)
            Cart.objects(id=id).update(**res)
            data = Cart.objects(id=id).first()
            json_obj = schemas.CartSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Cart.objects(id=id).delete()
        return jsonify(data)


class OrderResource(Resource):
    def get(self, id=None):
        if id:
            json_obj = schemas.OrderSchema().dumps(Order.objects(id=id).first())
        else:
            json_obj = schemas.OrderSchema(many=True).dumps(Order.objects.all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = schemas.OrderSchema().loads(json_data)
            Order.objects.create(**res)
            res = json.loads(schemas.OrderSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = schemas.OrderSchema().loads(json_data)
            Order.objects(id=id).update(**res)
            data = Order.objects(id=id).first()
            json_obj = schemas.OrderSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Order.objects(id=id).delete()
        return jsonify(data)


class TotalResource(Resource):
    def get(self):
        data = Products.objects.all()
        agr = 0
        if len(data):
            for row in data:
                agr += row.price

            agr = round(agr / len(data), 2)

        return jsonify(agr)
