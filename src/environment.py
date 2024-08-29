import os
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(FOLDER_PATH, "../../..", ".env")


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, frozen=True)
    detector_used: str = Field(
        validation_alias=AliasChoices("DETECTOR_USED", "DETECTOR-USED"),
        default="YOLOV8",
    )
    route_prefix: str = Field(
        validation_alias=AliasChoices("ROUTE_PREFIX", "ROUTE-PREFIX"),
        default="",
    )
    debug_mode: bool = Field(
        validation_alias=AliasChoices("DEBUG_MODE", "DEBUG-MODE"),
        default=False,
    )
