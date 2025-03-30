# Audio Upload Service

Сервис для загрузки и обработки аудио файлов с авторизацией через Яндекс OAuth.

## Требования

- Docker
- Docker Compose

## Развертывание

1. **Клонирование репозитория**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   ```
   Отредактируйте файл `.env` и укажите:
   - Учетные данные для PostgreSQL
   - Данные приложения Яндекс OAuth (получите их на https://oauth.yandex.ru)
   - Секретный ключ для JWT
   - Учетные данные для MinIO
   - Email администратора

3. **Запуск сервисов**
   ```bash
   docker-compose up --build
   ```

   Это запустит:
   - FastAPI приложение на порту 8000
   - PostgreSQL на порту 5432
   - MinIO на порту 9000

4. **Проверка работоспособности**
   - Swagger UI: http://localhost:8000/docs
   - MinIO Console: http://localhost:9000

## Переменные окружения

### PostgreSQL
- `POSTGRES_SERVER`: Хост базы данных
- `POSTGRES_USER`: Имя пользователя
- `POSTGRES_PASSWORD`: Пароль
- `POSTGRES_DB`: Название базы данных
- `POSTGRES_PORT`: Порт (по умолчанию 5432)

### Yandex OAuth
- `YANDEX_CLIENT_ID`: ID приложения Яндекс OAuth
- `YANDEX_CLIENT_SECRET`: Секретный ключ приложения
- `SERVER_DOMAIN`: Домен сервера для callback URL

### JWT
- `SECRET_KEY`: Секретный ключ для подписи токенов
- `ALGORITHM`: Алгоритм подписи
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Время жизни access token
- `REFRESH_TOKEN_EXPIRE_DAYS`: Время жизни refresh token

### MinIO
- `MINIO_HOST`: Адрес сервера MinIO
- `MINIO_ROOT_USER`: Имя пользователя
- `MINIO_ROOT_PASSWORD`: Пароль
- `MINIO_BUCKET_NAME`: Название бакета

### Admin
- `ADMIN_EMAIL`: Email администратора