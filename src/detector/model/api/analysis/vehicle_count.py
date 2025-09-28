from pydantic import Field

from common.model import ResponseBase


class VehicleCountResponse(ResponseBase):
    vehicles_total: int = Field(title="Total number of vehicles counted")
    motorbikes: int = Field(title="Number of motorbikes counted")
    cars: int = Field(title="Number of cars counted")
    buses: int = Field(title="Number of buses counted")
    trucks: int = Field(title="Number of trucks counted")
    bicycles: int = Field(title="Number of bicycles counted")
