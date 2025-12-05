from datetime import datetime
from pydantic import BaseModel


class FileBase(BaseModel):
    original_name: str
    version: int
    size: int
    uploaded_at: datetime


class FileOut(FileBase):
    id: int

    class Config:
        from_attributes = True


class FileAnalysisOut(BaseModel):
    file_id: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True
