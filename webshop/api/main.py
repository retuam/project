from flask import Flask, Blueprint
from flask_restful import Api
from .resources import *


api_bp = Blueprint('api', __name__)
building_api = Api(api_bp)


@api_bp.route('/test')
def index():
    print(1)
    return f'2'


building_api.add_resource(
    TotalResource,
    '/',
)

building_api.add_resource(
    ProductResource,
    '/product',
    '/product/category/<category_id>',
    '/product/<id>',
)

building_api.add_resource(
    ImageResource,
    '/upload/<id>'
)

building_api.add_resource(
    CategoryResource,
    '/category',
    '/category/<id>'
)

building_api.add_resource(
    SubcategoryResource,
    '/subcategory',
    '/subcategory/<id>'
)

building_api.add_resource(
    CartResource,
    '/cart',
    '/cart/<id>'
)

building_api.add_resource(
    OrderResource,
    '/order',
    '/order/<id>'
)

building_api.add_resource(
    TextResource,
    '/text',
    '/text/<id>'
)
