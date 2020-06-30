#Реализовать
1. Просмотр информации о продукте (изображение, описание, цена, скидка)   
2. Просмотр заказов в REST
3. При нажатии на кнопку "Корзина" выводить ее содержимое с общей стоимостью
4. После добавления товара в корзину должна быть возможность изменения количества товара.
5. Для одновременного существования бота и рест брать BluePrint

#STACK
1. Telebot
2. Flask (flask restfull)
3. MongoDB
4. VPS - virtual private server, Google Cloud
5. Webhook
6. Marshmallow

#Functionality
1. Бот  
1.1. Предоставлять пользователю список доступных категорий (с подкатегорями);    
1.2. Предоставлять пользователю список доступных продуктов, определенной категории   
1.3. Просмотр информации о продукте (изображение, описание, цена, скидка)   
1.4. Корзина    
1.5. Оформление заказов    
1.6. Просмотр содержимого корзины    
1.7. Просмотр продуктов со скидкой  
2. REST API  
2.1. Просмотр заказов   
2.2. CRUD

#Implementation
1. Категории
2. Продукты
3. Корзины
4. Пользователи бота
5. Тексты
6. Заказы
7. Админы

#Практика №1
1. Реализовать колекцию текстов (choices внутри колекцию)
2. Реализовать бот, который будет на старте 
- Приветствовать юзера 
- Отправлять список шаблонных кнопок (Товары со скидкой, категории, моя корзина) 
- Описать хэндлер к кнопке "категории" (InlineKeyboardMarkup)
3. Описать коллекцию юзера 
- При старте инициализировать юзера
4. Описать аттрибуты товара используя EmbededDocumentField

#Практика №3
1. Реализовать вывод категорий, в случае если выводимая категория содержит подкатегории, при килке на нее, замещать сообщение списком из подкатегорий (edit_message).
2. Если категория не содержит подкатегорий выводить ее продукты. Каждый продукт это - отдельное сообщение, состоящее из описании, тайтла и картинки.
3. Зарегистриоваться и ознакомиться с google.cloud (разобрать как создать ВМ)

#Практика №4
1. При клике на конечную категорию иерархии выводить все товары этой категории.
2. Создать экземпляр ВМ на Google Cloud. Требования к вм цп - 1 ядро ОП - 1.5 (с головой) памяти - 30 ОС - Ubuntu Server 18.04 сервер - расположение Европа
 
#Практика #5
1. При клике на кнопку добавить в корзину - добавлять товар в корзину. (Добавить эту кнопку к каждому продукту при выводе)
2. При нажатии на кнопку "Корзина" выводить ее содержимое с общей стоимостью. 
3. После добавления товара в корзину должна быть возможность изменения количества товара.
4. Если категория не рут добавить кнопку "Назад", которая будет возвращать к списку категорий.

#Практика №6
1. Реализовать REST доступ к приложению + валидация.
2. Для одновременного существования бота и рест брать BluePrint
3. Возможность оформление заказа. (Подтверждение корзины)