"""SQLAlchemy base declarative model for all database tables.

Provides the shared Base class that all database models inherit from.
"""

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase

meta = sa.MetaData()


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
