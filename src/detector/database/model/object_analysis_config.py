from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from common.database import Base


class ObjectAnalysisConfig(Base):
    __tablename__ = "object_analysis_config"

    account_id: Mapped[UUID] = mapped_column(
        "account_uuid", nullable=False,
    )
    config_name: Mapped[str] = mapped_column(
        "config_name", nullable=True,
    )
    example_image_id: Mapped[UUID] = mapped_column(
        "example_image_uuid", nullable=False,
    )
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
        return f"ObjectAnalysisConfig(account={self.account_id},image_resolution_width={self.image_resolution_width},image_resolution_height={self.image_resolution_height},confidence={self.confidence})"
