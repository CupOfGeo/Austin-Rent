from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa

meta = sa.MetaData()


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
