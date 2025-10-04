from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# local imports
from common.database import Base


class FrameMask(Base):
    __tablename__ = "frame_mask"

    pixel_width: Mapped[int] = mapped_column(
        "pixel_width", nullable=False
    )
    pixel_height: Mapped[int] = mapped_column(
        "pixel_height", nullable=False
    )
    object_analysis_config: Mapped[UUID] = mapped_column(
        "object_analysis_config_uuid", ForeignKey("object_analysis_config.uuid", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self) -> str:
        return f"FrameMask(pixel_width={self.pixel_width},pixel_height={self.pixel_height},object_analysis_config={self.object_analysis_config})"
