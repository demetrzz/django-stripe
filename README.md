# Django with Stripe
## Стек:
* Python 3.11
* Django 4/
* DjangoRestFramework
* PostgreSQL
* Docker
* Gunicorn
* Nginx
## Установка проекта
1. склонировать проект на сервер
2. создать файл .env в корне проекта по примеру, добавить домен/ip вашего сервера в ALLOWED_HOSTS:
```commandline
STRIPE_PUBLISHABLE_KEY=your_key
STRIPE_SECRET_KEY=your_key
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_DB=db
DB_NAME=stripeproject
DB_USER=your_user
DB_PASSWORD=your_password
POSTGRES_DB=stripeproject
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS=0.0.0.0 127.0.0.1 localhost [::1]
SECRET_KEY=your_key
```
3. создать и запустить контейнеры, миграции, создать супер юзера, запустить тесты:
```
docker compose build
docker compose up
docker exec -t -i container_id
python manage.py migrate
python manage.py createsuperuser
python manage.py test
```


## Наполнение базы товарами через админку:
* Залогиниться на созданного супер юзера: /admin
* Добавить товары в Items
* Создать объекты налога, скидок в Tax, Discount
* Создать объект заказа Order
* Order наполняется при помощи модели OrderItem

## Оплата:
* Перейти по /order/id/, где ID это id заказа
* Ввести тестовые данные:
* номер карты: 5555 5555 5555 4444
* дата: 12/24
* CVV: 000
* ZIP: 00000
* При успешной оплате:
1) Кнопка покупки станет неактивной, придет сообщение об успешной оплате:
![alt text](https://i.imgur.com/WGxI4bJ.png)
2) Придет успешный запрос на тестовый API Stripe
![alt text](https://i.imgur.com/rkly9Ax.png)

### По умолчанию используется Stripe Payment Intent, версия view с использованием Stripe Session, в этом случае будет редирект на страницу оплаты в Stripe:
```
class BuyOrderViewSession(APIView):
    def get(self, request, **kwargs):
        order = get_object_or_404(Order, id=kwargs['id'])
        stripe.api_key = settings.STRIPE_SECRET_KEY

        total_amount = order.total_amount

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Order ' + str(order.id),
                    },
                    'unit_amount': int(total_amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
        )

        return Response({'session_id': session.id})
```

### Краткая документация по эндпоинтам:
1. buy/order/<int:id>/ :
Принимает id заказа, открывает темплейт order.html


2. order/<int:id>/ :
Здесь осноная бизнес логика, вызывается в order.html, возвращает в него client_id