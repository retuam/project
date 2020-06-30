from marshmallow import Schema, fields, validate, validates, ValidationError


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=1, max=512)])
    description = fields.String(required=True, validate=[validate.Length(min=2, max=4096)])


class SubcategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=1, max=512)])
    description = fields.String(required=True, validate=[validate.Length(min=2, max=4096)])
    parent = fields.Nested(CategorySchema, required=True)


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=3, max=512)])
    description = fields.String(required=True, validate=[validate.Length(min=2, max=4096)])
    created = fields.DateTime(dump_only=True, required=True)
    price = fields.Float(default=0)
    discount = fields.Integer(dump_only=True, default=0)
    in_stock = fields.Boolean(default=True)
    category = fields.Nested(CategorySchema, required=True)
    image = fields.Field()
    attributes = fields.Field()


class UserSchema(Schema):
    title = fields.String(required=True, validate=[validate.Length(min=1, max=512)])
    is_moderator = fields.Boolean(default=True)
    uid = fields.Integer(dump_only=True, default=0)


class CartSchema(Schema):
    user = fields.Nested(UserSchema, required=True)
    products = fields.List(fields.Nested(ProductSchema, required=True))


class OrderSchema(Schema):
    user = fields.Nested(UserSchema, required=True)
    products = fields.List(fields.Nested(ProductSchema, required=True))
    created = fields.DateTime(dump_only=True, required=True)
