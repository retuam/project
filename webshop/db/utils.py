from models import Text


def init_texts():
    Text.objects.create(
        title=Text.TITLES['greetings'],
        body='Рады приветсвовать Вас в нашем интернет магазине'
    )
    Text.objects.create(
        title=Text.TITLES['cart'],
        body='Вы перешли в корзину'
    )


def init_texts_next():
    Text.objects.create(
        title=Text.TITLES['to_cart'],
        body='Вы добавляете товар в корзину'
    )
    Text.objects.create(
        title=Text.TITLES['from_cart'],
        body='Вы перешли в корзину'
    )
    Text.objects.create(
        title=Text.TITLES['category'],
        body='Вы выбрали категорию'
    )
    Text.objects.create(
        title=Text.TITLES['add'],
        body='Вы добавили товар в корзину'
    )
    Text.objects.create(
        title=Text.TITLES['erase'],
        body='Вы очистили корзину'
    )
    Text.objects.create(
        title=Text.TITLES['checkout'],
        body='Вы оплатили товары'
    )
    Text.objects.create(
        title=Text.TITLES['empty'],
        body='Ваша корзина пуста'
    )
    Text.objects.create(
        title=Text.TITLES['discount'],
        body='Вы выбрали товары со скидкой'
    )
    Text.objects.create(
        title=Text.TITLES['finish'],
        body='Вы завершаете покупку'
    )


if __name__ == '__main__':
    # init_texts()
    init_texts_next()
