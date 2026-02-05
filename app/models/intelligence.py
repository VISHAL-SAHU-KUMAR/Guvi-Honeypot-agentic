# Intelligence extraction models

from pydantic import BaseModel
from typing import List

class Intelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phoneNumbers: List[str] = []
    phishingLinks: List[str] = []
    suspiciousKeywords: List[str] = []