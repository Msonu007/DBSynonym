from typing import List, Optional
from sqlmodel import SQLModel, Field
import json


class Synonym(SQLModel, table=True):
    """Synonym table definition.

    synonyms are stored as JSON‑encoded list of strings for portability across DBs."""

    word_id: int = Field(primary_key=True, index=True)
    word: str = Field(index=True, max_length=255)
    synonyms_json: str = Field(sa_column_kwargs={"nullable": False})

    # Convenience property
    @property
    def synonyms(self) -> List[str]:
        return json.loads(self.synonyms_json)
