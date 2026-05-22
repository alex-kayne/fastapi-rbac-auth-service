from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint, Text, Integer, Boolean, DateTime
from sqlalchemy.orm import mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin, CreatedAtMixin, Mapped


class User(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    full_name: str = mapped_column(Text, nullable=False)
    email: str = mapped_column(Text, unique=True, index=True, nullable=False)
    hashed_password: str = mapped_column(Text, nullable=False)
    is_active: bool = mapped_column(Boolean, default=True, nullable=False)
    sessions: Mapped[list["UserSession"]] = relationship()
    roles: Mapped[list["UserRole"]] = relationship()


class UserSession(Base, IdMixin, TimestampMixin):
    __tablename__ = "user_sessions"

    user_id: int = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token_jti: str = mapped_column(Text, unique=True, index=True, nullable=False)
    is_active: bool = mapped_column(Boolean, default=True, nullable=False)
    expires_at: datetime = mapped_column(DateTime(timezone=True), nullable=False)


class Role(Base, IdMixin, TimestampMixin):
    __tablename__ = "roles"

    name: str = mapped_column(Text, unique=True, index=True, nullable=False)
    description: str = mapped_column(Text, nullable=True)
    users: Mapped[list["UserRole"]] = relationship()
    permissions: Mapped[list["RolePermission"]] = relationship()


class Resource(Base, IdMixin, TimestampMixin):
    __tablename__ = "resources"

    code: str = mapped_column(Text, unique=True, index=True, nullable=False)
    name: str = mapped_column(Text, nullable=False)
    permissions: Mapped[list["Permission"]] = relationship()


class Permission(Base, IdMixin, TimestampMixin):
    __tablename__ = "permissions"

    resource_id: int = mapped_column(Integer, ForeignKey("resources.id"), nullable=False)
    resource: Mapped["Resource"] = relationship()
    action: str = mapped_column(Text, nullable=False)
    code: str = mapped_column(Text, unique=True, index=True, nullable=False)
    description: str = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("resource_id", "action", name="uq_resource_id_action"),
    )


class UserRole(Base, CreatedAtMixin):
    __tablename__ = "user_roles"

    user_id: int = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    role_id: int = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "role_id", name="pk_user_id_role_id"),
    )


class RolePermission(Base, CreatedAtMixin):
    __tablename__ = "role_permissions"

    role_id: int = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id: int = mapped_column(Integer, ForeignKey("permissions.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("role_id", "permission_id", name="pk_role_id_permission_id"),
    )
