# models.py
# models.py
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str
