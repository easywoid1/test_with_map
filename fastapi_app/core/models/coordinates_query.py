from . import Base, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Float


class CoordinatesQuery(TimestampMixin, Base):
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    radius: Mapped[float] = mapped_column(Float, nullable=False)
    result: Mapped[dict] = mapped_column(JSON, nullable=False)
