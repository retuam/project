from models import Category, Products, ProductsAttribute
from random import randint, choice


def seed_categories():
    category_title = ['Category 1', 'Category 2', 'Category 3', 'Category 4']
    category_description = ['Category description 1', 'Category description 2',
                            'Category description 3', 'Category description 4']
    for title, description in zip(category_title, category_description):
        Category.objects.create(title=title, description=description)


def seed_subcategories():
    category_title = ['Sub category 1', 'Sub category 2', 'Sub category 3', 'Sub category 4']
    category_description = ['Sub category description 1', 'Sub category description 2',
                            'Sub category description 3', 'Sub category description 4']
    for title, description in zip(category_title, category_description):
        Category.objects.create(title=title, description=description, parent=choice(Category.get_root_categories()))


def seed_add_subcategories():
    categories = Category.objects()
    for category in categories:
        if category.parent:
            category.parent.add_subcategory(category)


def seed_products():
    product_vendor = ['Vendor 1', 'Vendor 2', 'Vendor 3', 'Vendor 4']
    product_title = ['Product 1', 'Product 2', 'Product 3', 'Product 4']
    product_price = [100.10, 206.3, 307.7, 40.78]
    product_discount = [0, 10, 5, 15]
    product_in_stock = [True, True, False, True]
    product_description = ['Product description 1', 'Product description 2',
                           'Product description 3', 'Product description 4']
    for title, description, price, discount, in_stock, vendor in zip(product_title, product_description, product_price,
                                                                     product_discount, product_in_stock, product_vendor):
        Products.objects.create(attributes=ProductsAttribute(weight=randint(0, 10), height=randint(0, 100),
                                                             vendor=vendor), price=price, discount=discount,
                                in_stock=in_stock, title=title, description=description,
                                category=choice(Category.get_root_categories()))


def seed_products_child():
    products = Products.objects()
    for product in products:
        product.category = choice(Category.get_child_categories())
        product.save()


if __name__ == '__main__':
    seed_categories()
    seed_subcategories()
    seed_products()
    seed_add_subcategories()
    seed_products_child()
