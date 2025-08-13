# Receipts API

Это FastAPI-приложение для управления чеками.

## Запуск приложения

Для запуска приложения в режиме разработки используйте следующую команду:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Документация API

Интерактивная документация API доступна после запуска приложения:

-   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
-   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Эндпоинты API

API доступен по адресу `/api/v1/receipts`.

### Получить все чеки

-   **Эндпоинт:** `GET /api/v1/receipts/`
-   **Описание:** Получает список всех чеков.
-   **Ссылка для браузера:** [http://localhost:8000/api/v1/receipts/](http://localhost:8000/api/v1/receipts/)
-   **Команда cURL:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/receipts/" -H "accept: application/json"
    ```

### Получить чек по ID

-   **Эндпоинт:** `GET /api/v1/receipts/{receipt_id}`
-   **Описание:** Получает конкретный чек по его ID.
-   **Ссылка для браузера:** [http://localhost:8000/api/v1/receipts/1](http://localhost:8000/api/v1/receipts/1) (замените `1` на существующий ID чека)
-   **Команда cURL:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/receipts/1" -H "accept: application/json"
    ```

### Создать чек

-   **Эндпоинт:** `POST /api/v1/receipts/`
-   **Описание:** Создает новый чек.
-   **Команда cURL:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/receipts/" -H "accept: application/json" -H "Content-Type: application/json" -d '{
      "user_id": 1,
      "items": [
        {
          "name": "item1",
          "price": 100,
          "quantity": 1
        },
        {
          "name": "item2",
          "price": 200,
          "quantity": 2
        }
      ]
    }'
    ```
