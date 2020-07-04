import mongoengine as me
import datetime


me.connect('webshop_adv_april_new')


class Category(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self', default=None)

    def add_subcategory(self, category: 'Category'):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()

    def get_products(self):
        return Products.objects(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @classmethod
    def get_child_categories(cls):
        return cls.objects(parent__ne=None)

    @property
    def is_parent(self) -> bool:
        return bool(self.subcategories)


class ProductsAttribute(me.EmbeddedDocument):
    weight = me.IntField()
    height = me.IntField()
    vendor = me.StringField()


class Products(me.Document):
    attributes = me.EmbeddedDocumentField(ProductsAttribute)
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    created = me.DateTimeField(default=datetime.datetime.now())
    price = me.DecimalField(required=True)
    discount = me.IntField(min_length=0, max_length=100)
    in_stock = me.BooleanField(default=True)
    image = me.FileField(required=True)
    category = me.ReferenceField('Category')

    @property
    def extended_price(self):
        return self.price * (100 - self.discount) / 100

    @classmethod
    def get_discounts_product(cls):
        return cls.objects(discount__ne=0, in_stock=True)


class User(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    is_moderator = me.BooleanField(default=False)
    uid = me.IntField(min_length=0)


class Cart(me.Document):
    user = me.ReferenceField('User')
    product = me.ReferenceField('Products')
    qty = me.IntField(default=1, min_length=1)
    price = me.DecimalField(required=True)

    @classmethod
    def price(cls):
        _sum = 0
        for product in cls.objects():
            _sum += product.price
        return _sum

    @classmethod
    def user_price(cls, user):
        _sum = 0
        for product in cls.objects(user=user):
            _sum += product.price
        return _sum


class Order(me.Document):
    user = me.ReferenceField('User')
    product = me.ReferenceField('Products')
    qty = me.IntField(default=1, min_length=1)
    price = me.DecimalField(required=True)
    created = me.DateTimeField(default=datetime.datetime.now())

    @classmethod
    def price(cls):
        _sum = 0
        for product in cls.objects():
            _sum += product.price
        return _sum

    @classmethod
    def user_price(cls, user):
        _sum = 0
        for product in cls.objects(user=user):
            _sum += product.price
        return _sum


class Text(me.Document):
    title = me.StringField(min_length=1, max_length=256, unique=True)
    slug = me.StringField(min_length=1, max_length=32, unique=True)
    body = me.StringField(min_length=1, max_length=4096)
