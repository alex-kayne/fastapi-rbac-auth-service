# FastAPI RBAC Auth Service

Backend-приложение на FastAPI с собственной системой аутентификации и авторизации на основе RBAC + permissions.

## Описание системы доступа

Система построена на трёх уровнях:

- **User** получает одну или несколько **Role**
- **Role** содержит набор **Permission**
- **Permission** описывает конкретное действие над ресурсом (`documents:read`, `orders:read`, `access_rules:manage`)

При каждом запросе backend проверяет JWT + активную запись в `user_sessions`. Logout инвалидирует сессию — старый токен перестаёт работать. Soft delete переводит пользователя в `is_active=False` и инвалидирует все его сессии.

## Tech stack

- Python 3.12+
- FastAPI
- PostgreSQL 16
- SQLAlchemy async + asyncpg
- Alembic
- Pydantic v2
- PyJWT + passlib/bcrypt
- Docker Compose

## Запуск

### Вариант 1 — Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Миграции применяются автоматически при старте контейнера.

### Вариант 2 — локально

```bash
cp .env.example .env
# заполнить .env своими значениями

poetry install
poetry run alembic upgrade head
poetry run fastapi dev app/main.py
```

## Seed

Заполнить БД тестовыми данными (роли, permissions, admin-пользователь):

```bash
# локально
poetry run python -m app.db.seed

# через Docker
docker compose run app python -m app.db.seed
```

После seed в БД появятся:

| Сущность | Значения |
|----------|----------|
| Resources | documents, reports, orders, access_rules |
| Permissions | documents:read, reports:read, orders:read, access_rules:manage |
| Roles | admin, user |
| Admin user | admin@example.com / admin123 |

## API

Документация доступна по адресу: `http://localhost:8000/docs`

### Auth

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Логин, возвращает JWT |
| POST | `/auth/logout` | Логаут, инвалидирует сессию |

### Users

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/users/me` | Профиль текущего пользователя |
| PATCH | `/users/me` | Обновить профиль |
| DELETE | `/users/me` | Soft delete аккаунта |

### Business resources (mock)

| Метод | URL | Требуемый permission |
|-------|-----|----------------------|
| GET | `/business/documents` | `documents:read` |
| GET | `/business/reports` | `reports:read` |
| GET | `/business/orders` | `orders:read` |

### Admin (требует `access_rules:manage`)

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/access/roles` | Список ролей |
| GET | `/access/permissions` | Список permissions |
| POST | `/access/role` | Создать роль |
| POST | `/access/users/{user_id}/roles/{role_id}` | Назначить роль пользователю |
| DELETE | `/access/users/{user_id}/roles/{role_id}` | Снять роль с пользователя |
| POST | `/access/roles/{role_id}/permissions/{permission_id}` | Назначить permission роли |
| DELETE | `/access/roles/{role_id}/permissions/{permission_id}` | Снять permission с роли |

## Сценарии проверки

**1. Регистрация и логин**
```
POST /auth/register — создать пользователя
POST /auth/login — получить токен
```

**2. Доступ без токена → 401**
```
GET /business/documents (без Authorization header) → 401
```

**3. Доступ без permission → 403**
```
GET /business/documents (токен обычного пользователя без роли) → 403
```

**4. Назначить роль через admin и проверить доступ**
```
POST /auth/login (admin@example.com / admin123) → получить admin-токен
POST /access/users/{user_id}/roles/2 → назначить роль user
POST /access/roles/2/permissions/{permission_id} → назначить permission
GET /business/documents (токен пользователя) → 200
```

**5. Logout — старый токен перестаёт работать**
```
POST /auth/logout → 200
GET /users/me (старый токен) → 401
```

**6. Soft delete — пользователь не может залогиниться**
```
DELETE /users/me → 204
POST /auth/login (те же credentials) → 401
```