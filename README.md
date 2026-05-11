# Shop_WB-Tech

REST API интернет-магазина на Django + DRF.

## Что делает проект

- Регистрация и JWT-авторизация пользователей
- Профиль пользователя и пополнение баланса
- Каталог товаров (чтение для всех, изменение только для админа)
- Корзина (добавить, изменить количество, удалить, посмотреть)
- Создание заказа из корзины с бизнес-проверками:
  - достаточно товара на складе
  - достаточно средств на балансе
  - списание остатков и баланса
  - очистка корзины
  - уведомление об успешном заказе (console email backend)


## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска:

- API: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

## Локальный запуск без Docker

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Запуск тестов

### Через Docker

```bash
docker compose exec web python manage.py test
```

### Локально

```bash
python manage.py test
```


