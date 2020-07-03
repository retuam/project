from models import Category, Products, ProductsAttribute
from random import randint, choice
import requests


def seed_categories():
    category_title = [f'Sub category {i}' for i in range(5)]
    category_description = [f'Sub category description {i}' for i in range(5)]
    for title, description in zip(category_title, category_description):
        Category.objects.create(title=title, description=description)


def seed_subcategories():
    category_title = [f'Sub category {i}' for i in range(15)]
    category_description = [f'Sub category description {i}' for i in range(15)]
    for title, description in zip(category_title, category_description):
        Category.objects.create(title=title, description=description, parent=choice(Category.get_root_categories()))


def seed_add_subcategories():
    categories = Category.objects()
    for category in categories:
        if category.parent:
            category.parent.add_subcategory(category)


def seed_products(name):
    product_vendor = [f'Vendor {i}' for i in range(5)] * 10
    product_title = [f'Product {i}' for i in range(50)]
    product_price = [randint(0, 1000) for _ in range(50)]
    product_discount = [choice([0, 10, 5, 0]) for _ in range(50)]
    product_in_stock = [choice([True, True, False, True]) for _ in range(50)]
    product_description = [f'Product {i} description...' for i in range(50)]
    for title, description, price, discount, in_stock, vendor in zip(product_title, product_description, product_price,
                                                                     product_discount, product_in_stock, product_vendor):
        product = Products(attributes=ProductsAttribute(weight=randint(0, 10), height=randint(0, 100), vendor=vendor),
                           price=price, discount=discount, in_stock=in_stock, title=title, description=description,
                           category=choice(Category.get_root_categories()))
        with open(name, 'rb') as image:
            product.image.put(image, content_type='image/jpeg')
        product.save()


def seed_products_child():
    products = Products.objects()
    for product in products:
        product.category = choice(Category.get_child_categories())
        product.save()


def download_file():
    url = 'https://miro.medium.com/max/1200/1*mk1-6aYaf_Bes1E3Imhc0A.jpeg'
    result = requests.get(url)
    ext = url.split('.')[-1]
    name = f'default.{ext}'
    with open(name, 'wb') as file:
        file.write(result.content)
    return name


if __name__ == '__main__':
    seed_categories()
    seed_subcategories()
    seed_products(download_file())
    seed_add_subcategories()
    seed_products_child()
