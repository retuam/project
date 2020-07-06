from models import Text


def init_texts():
    Text.objects.create(
        title='Текст приветствия',
        slug='greetings',
        body='Рады приветсвовать Вас в нашем интернет магазине'
    )
    Text.objects.create(
        title='В Вашей корзине следующие товары',
        slug='cart',
        body='Вы перешли в корзину'
    )
    Text.objects.create(
        title='Добавить в корзину',
        slug='to_cart',
        body='Вы добавляете товар в корзину'
    )
    Text.objects.create(
        title='Для удаления товара из корзины, выберите товар',
        slug='from_cart',
        body='Вы перешли в корзину'
    )
    Text.objects.create(
        title='Выберите категорию',
        slug='category',
        body='Выберите категорию'
    )
    Text.objects.create(
        title='Товар добавлен в корзину',
        slug='add',
        body='Вы добавили товар в корзину'
    )
    Text.objects.create(
        title='Очищено',
        slug='erase',
        body='Вы очистили корзину'
    )
    Text.objects.create(
        title='Оплачено',
        slug='checkout',
        body='Вы оплатили товары'
    )
    Text.objects.create(
        title='Корзина пуста',
        slug='empty',
        body='Ваша корзина пуста'
    )
    Text.objects.create(
        title='Товар удален',
        slug='product_empty',
        body='Вы удалили товар из корзины'
    )
    Text.objects.create(
        title='Товары со скидкой',
        slug='discount',
        body='Вы выбрали товары со скидкой'
    )
    Text.objects.create(
        title='Для завершения покупки нажмите "Оплата", для очистки корзины нажмите "Очистить"',
        slug='finish',
        body='Вы завершаете покупку'
    )
    Text.objects.create(
        title='Товары отсутствуют',
        slug='empty_cat',
        body='Категория пуста'
    )
    Text.objects.create(
        title='Общая стоимость',
        slug='total',
        body='Общая стоимость'
    )
    Text.objects.create(
        title='Просмотр товара',
        slug='product',
        body='Вы просматриваете карточку товара'
    )
    Text.objects.create(
        title='Изменение количества',
        slug='change',
        body='Для добавления товара нажимете "+", для уменьшение товара нажмите "-", для удаление нажмите "x"'
    )
    Text.objects.create(
        title='Назад',
        slug='back',
        body='Назад'
    )


if __name__ == '__main__':
    init_texts()
