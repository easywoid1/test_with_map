from typing import Annotated

from pydantic import BaseModel, Field


class CoordinatesBase(BaseModel):
    latitude: Annotated[float, Field(ge="-90", le="90")]
    longitude: Annotated[float, Field(ge="-180", le="180")]
    radius: Annotated[float, Field(ge=0)]


class CoordinatesResponse(CoordinatesBase):
    result: dict
