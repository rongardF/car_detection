from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base

# local imports
from ...model.enum import ObjectEnum


class Object(Base):
    __tablename__ = "object"

    value: Mapped[ObjectEnum] = mapped_column(
        "value", nullable=False
    )
    count_analysis_config: Mapped[UUID] = mapped_column(
        "count_analysis_config_uuid", ForeignKey("count_analysis_config.uuid", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self) -> str:
        return f"Object(value={self.value},count_analysis_config={self.count_analysis_config})"
