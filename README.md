# FastAPI RBAC Auth Service

Backend-приложение на FastAPI с собственной системой аутентификации и авторизации.

Проект выполнен как тестовое задание. Основная цель — показать проектирование системы доступа к ресурсам: пользователи, роли, permissions, ресурсы и действия.

## Tech stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy async
- Alembic
- Pydantic v2
- JWT / sessions
- passlib / bcrypt
- Docker Compose
- pytest

## Features

### User module

- User registration
- Login by email and password
- Logout
- Get current user profile
- Update user profile

### Access control module

Main entities:

- `users`
- `roles`
- `resources`
- `permissions`
- `user_roles`
- `role_permissions`
- `user_sessions`
