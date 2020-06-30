from flask import Flask
from flask_restful import Api
from .resources import *


app = Flask(__name__)
api = Api(app)

api.add_resource(
    TotalResource,
    '/',
)

api.add_resource(
    ProductResource,
    '/product',
    '/product/category/<category_id>',
    '/product/subcategory/<subcategory_id>',
    '/product/<id>'
)

api.add_resource(
    CategoryResource,
    '/category',
    '/category/<id>'
)

api.add_resource(
    SubcategoryResource,
    '/subcategory',
    '/subcategory/<id>'
)

api.add_resource(
    CartResource,
    '/cart',
    '/cart/<id>'
)

api.add_resource(
    OrderResource,
    '/order',
    '/order/<id>'
)

if __name__ == '__main__':
    app.run(debug=True)
