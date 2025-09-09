from sqlalchemy.orm import Mapped, mapped_column

from common.database import Base


class CountAnalysisConfig(Base):
    __tablename__ = "count_analysis_config"

    image_resolution_width: Mapped[int] = mapped_column(
        "resolution_width", nullable=False
    )
    image_resolution_height: Mapped[int] = mapped_column(
        "resolution_height", nullable=False
    )
    confidence: Mapped[float] = mapped_column(
        "confidence", nullable=False
    )

    def __repr__(self) -> str:
        return f"CountAnalysisConfig(image_resolution_width={self.image_resolution_width},image_resolution_height={self.image_resolution_height},confidence={self.confidence})"
