from typing import Annotated

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

INT_PRIMARY_KEY = Annotated[int, mapped_column(Integer, primary_key=True)]
