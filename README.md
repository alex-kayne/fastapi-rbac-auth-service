# FastAPI RBAC Auth Service

Backend-приложение на FastAPI с собственной системой аутентификации и авторизации.

Проект выполнен как тестовое задание. Основная цель — показать проектирование системы доступа к ресурсам: пользователи, роли, permissions, ресурсы и действия.

Система разделяет authentication и authorization. JWT используется для идентификации пользователя, а таблица user_sessions позволяет реализовать logout. Доступ к ресурсам управляется через RBAC: пользователь получает роли, роли содержат permissions, permission описывает действие над ресурсом.
Удаление пользователя реализовано через users.is_active=False. Такой пользователь сохраняется в БД, но больше не может войти в систему.

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
