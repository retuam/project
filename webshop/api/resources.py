from flask_restful import Resource
from .schemas import *
from ..db.models import *
from flask import request, jsonify
import json
from marshmallow import ValidationError


class CategoryResource(Resource):

    def get(self, id=None):
        if id:
            json_obj = CategorySchema().dumps(Category.objects(id=id).first())
        else:
            json_obj = CategorySchema(many=True).dumps(Category.get_root_categories().all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = CategorySchema().loads(json_data)
            Category.objects.create(**res)
            res = json.loads(CategorySchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = CategorySchema().loads(json_data)
            Category.objects(id=id).update(**res)
            data = Category.objects(id=id).first()
            json_obj = CategorySchema().dumps(data)
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
            json_obj = CategorySchema().dumps(Category.objects(id=id).first())
        else:
            json_obj = CategorySchema(many=True).dumps(Category.get_child_categories().all())
        return jsonify(json.loads(json_obj))

    def post(self):
        my_dict = request.json
        try:
            _parent = Category.objects(id=my_dict['parent_id']).first()
            _category = CategorySchema(only=("title", "description",)).dumps(_parent)

            my_dict['parent'] = json.loads(_category)
            my_dict.pop('parent_id', None)

            json_data = json.dumps(my_dict)

            res = SubcategorySchema().loads(json_data)
            res['parent'] = _parent
            Category.objects.create(**res)
            res = json.loads(SubcategorySchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        my_dict = request.json
        try:
            _parent = Category.objects(id=my_dict['parent_id']).first()
            _category = CategorySchema(only=("title", "description",)).dumps(_parent)

            my_dict['parent'] = json.loads(_category)
            my_dict.pop('parent_id', None)

            json_data = json.dumps(my_dict)

            res = SubcategorySchema().loads(json_data)
            res['parent'] = _parent
            Category.objects(id=id).update(**res)
            data = Category.objects(id=id).first()
            json_obj = SubcategorySchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Category.objects(id=id).delete()
        return jsonify(data)


class ProductResource(Resource):

    def get(self, id=None, category_id=None):
        if id:
            post = Products.objects(id=id).first()
            json_obj = ProductSchema().dumps(post)
        elif category_id:
            _category = Category.objects(id=category_id).first()
            json_obj = ProductSchema(many=True).dumps(Products.objects.filter(category=_category).all())
        else:
            json_obj = ProductSchema(many=True).dumps(Products.objects.all())

        return jsonify(json.loads(json_obj))

    def post(self):
        my_dict = request.json
        try:
            _parent = Category.objects(id=my_dict['category_id']).first()
            _category = CategorySchema(only=("title", "description",)).dumps(_parent)

            my_dict['category'] = json.loads(_category)
            my_dict.pop('category_id', None)

            json_data = json.dumps(my_dict)

            res = ProductSchema().loads(json_data)
            res['category'] = _parent
            Products.objects.create(**res)
            res = json.loads(ProductSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        my_dict = request.json
        try:
            _parent = Category.objects(id=my_dict['category_id']).first()
            _category = CategorySchema(only=("title", "description",)).dumps(_parent)

            my_dict['category'] = json.loads(_category)
            my_dict.pop('category_id', None)

            json_data = json.dumps(my_dict)

            res = ProductSchema().loads(json_data)
            res['category'] = _parent
            Products.objects(id=id).update(**res)
            data = Products.objects(id=id).first()
            json_obj = ProductSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Products.objects(id=id).delete()
        return jsonify(data)


class ImageResource(Resource):

    def post(self, id):
        image = request.files['image']
        try:
            product = Products.objects(id=id).first()
            product.image.put(image, content_type='image/jpeg')
            product.save()
            res = jsonify(json.loads(ProductSchema().dumps(product)))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        product = Products.objects(id=id).first()
        res = product.image.delete()
        product.save()
        return jsonify(res)


class CartResource(Resource):

    def get(self, id=None):
        if id:
            json_obj = CartSchema().dumps(Cart.objects(id=id).first())
        else:
            json_obj = CartSchema(many=True).dumps(Cart.objects.all())
        return jsonify(json.loads(json_obj))

    def post(self):
        my_dict = request.json
        try:
            _product = Products.objects(id=my_dict['product_id']).first()
            _product_dump = ProductSchema(only=("title", "category", "description",)).dumps(_product)

            my_dict['product'] = json.loads(_product_dump)
            my_dict.pop('product_id', None)

            _user = User.objects(id=my_dict['user_id']).first()
            _user_dump = UserSchema(only=("title",)).dumps(_user)

            my_dict['user'] = json.loads(_user_dump)
            my_dict.pop('user_id', None)

            json_data = json.dumps(my_dict)

            res = CartSchema().loads(json_data)
            res['product'] = _product
            Cart.objects.create(**res)
            res = json.loads(CartSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        my_dict = request.json
        try:
            _product = Products.objects(id=my_dict['product_id']).first()
            _product_dump = ProductSchema(only=("title",)).dumps(_product)

            my_dict['product'] = json.loads(_product_dump)
            my_dict.pop('product_id', None)

            _user = User.objects(id=my_dict['user_id']).first()
            _user_dump = UserSchema(only=("title",)).dumps(_user)

            my_dict['user'] = json.loads(_user_dump)
            my_dict.pop('user_id', None)

            json_data = json.dumps(my_dict)

            res = CartSchema().loads(json_data)
            res['product'] = _product
            Cart.objects(id=id).update(**res)
            data = Cart.objects(id=id).first()
            json_obj = CartSchema().dumps(data)
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
            json_obj = OrderSchema().dumps(Order.objects(id=id).first())
        else:
            json_obj = OrderSchema(many=True).dumps(Order.objects.all())
        return jsonify(json.loads(json_obj))

    def post(self):
        my_dict = request.json
        try:
            _product = Products.objects(id=my_dict['product_id']).first()
            _product_dump = ProductSchema(only=("title", "category", "description",)).dumps(_product)

            my_dict['product'] = json.loads(_product_dump)
            my_dict.pop('product_id', None)

            _user = User.objects(id=my_dict['user_id']).first()
            _user_dump = UserSchema(only=("title",)).dumps(_user)

            my_dict['user'] = json.loads(_user_dump)
            my_dict.pop('user_id', None)

            json_data = json.dumps(my_dict)

            res = OrderSchema().loads(json_data)
            res['product'] = _product
            Order.objects.create(**res)
            res = json.loads(OrderSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        my_dict = request.json
        try:
            _product = Products.objects(id=my_dict['product_id']).first()
            _product_dump = ProductSchema(only=("title",)).dumps(_product)

            my_dict['product'] = json.loads(_product_dump)
            my_dict.pop('product_id', None)

            _user = User.objects(id=my_dict['user_id']).first()
            _user_dump = UserSchema(only=("title",)).dumps(_user)

            my_dict['user'] = json.loads(_user_dump)
            my_dict.pop('user_id', None)

            json_data = json.dumps(my_dict)

            res = OrderSchema().loads(json_data)
            res['product'] = _product
            Order.objects(id=id).update(**res)
            data = Order.objects(id=id).first()
            json_obj = OrderSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Order.objects(id=id).delete()
        return jsonify(data)


class TextResource(Resource):

    def get(self, id=None):
        if id:
            json_obj = TextSchema().dumps(Text.objects(slug=id).first())
        else:
            json_obj = TextSchema(many=True).dumps(Text.objects.all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = TextSchema().loads(json_data)
            Text.objects.create(**res)
            res = json.loads(TextSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = TextSchema().loads(json_data)
            Text.objects(slug=id).update(**res)
            data = Text.objects(slug=id).first()
            json_obj = TextSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = Text.objects(slug=id).delete()
        return jsonify(data)


class UserResource(Resource):

    def get(self, id=None):
        if id:
            json_obj = UserSchema().dumps(User.objects(slug=id).first())
        else:
            json_obj = UserSchema(many=True).dumps(User.objects.all())
        return jsonify(json.loads(json_obj))

    def post(self):
        json_data = json.dumps(request.json)
        try:
            res = UserSchema().loads(json_data)
            User.objects.create(**res)
            res = json.loads(UserSchema().dumps(res))
        except ValidationError as err:
            res = err.messages
        return res

    def put(self, id):
        json_data = json.dumps(request.json)
        try:
            res = UserSchema().loads(json_data)
            User.objects(slug=id).update(**res)
            data = User.objects(slug=id).first()
            json_obj = UserSchema().dumps(data)
            res = jsonify(json.loads(json_obj))
        except ValidationError as err:
            res = err.messages
        return res

    def delete(self, id):
        data = User.objects(slug=id).delete()
        return jsonify(data)


class TotalResource(Resource):

    def get(self):
        data = Products.objects.all()
        agr = 0
        result = 0
        if len(data):
            for row in data:
                agr += row.price

            result = round(agr / len(data), 2)

        return float(result)
