from sqlmodel import SQLModel, Field

class CachedResult(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    original_string: str = Field(index=True, unique=True)
    transformed_string: str

class Payload(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    output: str
    