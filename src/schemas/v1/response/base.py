from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    class Config:
        use_enum_values = True


class ResponseEmpty(ResponseBase):
    result: bool = Field(True)
