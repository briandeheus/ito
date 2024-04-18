import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_on: datetime.datetime

    def format_created_on(self):
        return self.created_on.replace(tzinfo=datetime.timezone.utc).isoformat()
