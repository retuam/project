from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=1, max=512)], unique=True)
    description = fields.String(required=True, validate=[validate.Length(min=2, max=4096)])


class SubcategorySchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=1, max=512)], unique=True)
    description = fields.String(required=True, validate=[validate.Length(min=2, max=4096)])
    parent = fields.Nested(CategorySchema, required=True)


class ProductsAttributeSchema(Schema):
    weight = fields.Integer()
    height = fields.Integer()
    vendor = fields.String()


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=3, max=512)])
    description = fields.String(required=True, validate=[validate.Length(min=2, max=4096)])
    created = fields.DateTime(dump_only=True, required=True)
    price = fields.Float(default=0)
    discount = fields.Integer(default=0)
    in_stock = fields.Boolean(default=True)
    category = fields.Nested(CategorySchema, required=True)
    attributes = fields.Nested(ProductsAttributeSchema)


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=[validate.Length(min=1, max=512)])
    is_moderator = fields.Boolean(default=True)
    uid = fields.Integer(dump_only=True, default=0)


class CartSchema(Schema):
    id = fields.String(dump_only=True)
    # user = fields.Nested(UserSchema, required=True)
    product = fields.Nested(ProductSchema, required=True)
    price = fields.Float(default=0)
    qty = fields.Integer(default=1, min=1)


class OrderSchema(Schema):
    id = fields.String(dump_only=True)
    user = fields.Nested(UserSchema, required=True)
    product = fields.Nested(ProductSchema, required=True)
    price = fields.Float(default=0)
    qty = fields.Integer(default=1, min=1)
    created = fields.DateTime(dump_only=True, required=True)


class TextSchema(Schema):
    title = fields.String(required=True, validate=[validate.Length(min=1, max=256)])
    slug = fields.String(required=True, validate=[validate.Length(min=1, max=32)])
    body = fields.String(required=True, validate=[validate.Length(min=1, max=4096)])
