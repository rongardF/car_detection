from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.database import Base

# local imports
from .frame_mask import FrameMask
from .object import Object


class CountAnalysisConfig(Base):
    __tablename__ = "count_analysis_config"

    image_resolution_width: Mapped[int] = mapped_column(
        "resolution_width", nullable=False
    )
    image_resolution_height: Mapped[int] = mapped_column(
        "resolution_height", nullable=False
    )
    
    mask: Mapped[list[FrameMask]] = relationship()
    objects: Mapped[list[Object]] = relationship()

    def __repr__(self) -> str:
        return f"CountAnalysisConfig(image_resolution_width={self.image_resolution_width},image_resolution_height={self.image_resolution_height}),mask={self.mask},objects={self.objects}"
