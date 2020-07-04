from flask import Flask
#, Blueprint
from flask_restful import Api
from webshop.api.resources import *


# api_bp = Blueprint('api', __name__)
# api = Api(api_bp)

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
    '/product/<id>',
)

api.add_resource(
    ImageResource,
    '/upload/<id>'
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

api.add_resource(
    TextResource,
    '/text',
    '/text/<id>'
)

if __name__ == '__main__':
    app.run(debug=True)
