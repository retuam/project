import mongoengine as me
import datetime


me.connect('webshop_adv_april')


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
    products = me.ListField(me.ReferenceField('Products'))

    def add_products(self, product: 'Products'):
        self.products.append(product)
        self.save()

    def delete_products(self, product: 'Products'):
        self.products.pop(product)
        self.save()

    def price(self):
        _sum = 0
        for product in self.products:
            _sum += product.extended_price()
        return _sum


class Order(me.Document):
    user = me.ReferenceField('User')
    products = me.ListField(me.ReferenceField('Products'))
    created = me.DateTimeField(default=datetime.datetime.now())


class Text(me.Document):

    TITLES = {
        'greetings': 'Текст приветствия',
        'cart': 'В Вашей корзине следующие товары',
        'to_cart': 'Добавить в корзину',
        'from_cart': 'Для удаления товара из корзины, выберите товар',
        'category': 'Выберите категорию',
        'add': 'Товар добавлен в корзину',
        'erase': 'Очищено',
        'checkout': 'Оплачено',
        'empty': 'Корзина пуста',
        'discount': 'Товары со скидкой',
        'empty_sub': 'Товары и подкатегории отсутствуют',
        'empty_cat': 'Товары отсутствуют',
        'finish': 'Для завершения покупки нажмите "Оплата", для очистки корзины нажмите "Очистить"',
    }

    title = me.StringField(min_length=1, max_length=256, choices=TITLES.values(), unique=True)
    body = me.StringField(min_length=1, max_length=4096)
