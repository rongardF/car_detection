from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
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
    count_analysis_uuid: Mapped[UUID] = mapped_column(
        "count_analysis_config_uuid", ForeignKey("count_analysis_config.uuid", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self) -> str:
        return f"FrameMask(pixel_width={self.pixel_width},pixel_height={self.pixel_height},count_analysis_uuid={self.count_analysis_uuid})"
