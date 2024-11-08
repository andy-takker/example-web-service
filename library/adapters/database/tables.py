from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from library.adapters.database.base import BaseTable, IdentifableMixin, TimestampedMixin


class BookTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)


class UserTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
