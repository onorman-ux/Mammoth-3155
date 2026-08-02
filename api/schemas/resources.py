from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
class ResourceBase(BaseModel):
    item: str
    amount: Decimal = Field(ge=0)
    unit: str
class ResourceCreate(ResourceBase): pass
class ResourceUpdate(BaseModel):
    item: Optional[str]=None
    amount: Optional[Decimal]=Field(default=None, ge=0)
    unit: Optional[str]=None
class Resource(ResourceBase):
    id:int
    model_config=ConfigDict(from_attributes=True)
