from typing import List

import pydantic


class PrivacyText(pydantic.BaseModel):
    text: str | List[str] = ""
