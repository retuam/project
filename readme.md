#STACK:

Telebot
Flask (flask restfull)
MongoDB
VPS - virtual private server, Google Cloud
Webhook
Marshmallow
#Functionality

Бот 1.1. Предоставлять пользователю список доступных категорий (с подкатегорями); 1.2. Предоставлять пользователю список доступных продуктов, определенной категории 1.3. Просмотр информации о продукте (изображение, описание, цена, скидка) 1.4. Корзина 1.5. Оформление заказов 1.6. Просмотр содержимого корзины 1.7. Просмотр продуктов со скидкой
REST API 2.1. Просмотр заказов 2.2. CRUD
#Implementation

Категории
Продукты
Корзины
Пользователи бота
Тексты
Заказы
Админы
#Практика №1

Реализовать колекцию текстов (choices внутри колекцию)
Реализовать бот, который будет на старте 2.1. Приветствовать юзера 2.2. Отправлять список шаблонных кнопок (Товары со скидкой, категории, моя корзина) 2.3. Описать хэндлер к кнопке "категории" (InlineKeyboardMarkup)
Описать колекцию юзера 3.1. При старте инициализировать юзера
Описать аттрибуты товара используя EmbededDocumentField #Практика №3
Реализовать вывод категорий, в случае если выводимая категория содержит подкатегории, при килке на нее, замещать сообщение списком из подкатегорий (edit_message).
Если категория не содержит подкатегорий выводить ее продукты. Каждый продукт это - отдельное сообщение, состоящее из описании, тайтла и картинки.
Зарегистриоваться и ознакомиться с google.cloud (разобрать как создать ВМ) #Практика №4
При клике на коечную категорию иерархии выводить все товары этой категории.
Создать экземпляр ВМ на Google Cloud. Требования к вм цп - 1 ядро ОП - 1.5 (с головой) памяти - 30 ОС - Ubuntu Server 18.04 сервер - расположение Европа #Практика #5
При клике на кнопку добавить в корзину - добавлять товар в корзину. (Добавить эту кнопку к каждому продукту при выводе)
При нажатии на кнопку "Корзина" выводить ее содержимое с общей стоимостью. 3*) После добавления товара в корзину должна быть возможность изменения количества товара.
Если категория не рут добавить кнопку "Назад", которая будет возвращать к списку категорий.
#Практика №6

Реализовать REST доступ к приложению + валидация.
Для одновременного существования бота и рест брать BluePrint
Возможность оформление заказа. (ПОдтверждение корзины)