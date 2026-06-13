from pydantic import BaseModel
from typing import Literal

class SentimentSchema(BaseModel):
    sentiment:Literal["positive","negative","neutral"]