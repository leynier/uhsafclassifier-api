from typing import *
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Options(str, Enum):
    causes_deceased = "causes_deceased"
    causes_no_dir = "causes_no_dir"
    causes_quantity = "causes_quantity"
    causes_distance = "causes_distance"
    causes_low_quality = "causes_low_quality"
    causes_price = "causes_price"

class PersonModel(BaseModel):
    id: int
    date: datetime = None
    municipality: str = ""
    saf: str = ""
    full_name: str = ""
    ci: str = ""
    direction: str = ""
    attend_daily: bool = False
    attend_regular: bool = False
    attend_ocasional: bool = False
    dont_attend: bool = False
    service_qual_high: bool = False
    service_qual_medium: bool = False
    service_qual_low: bool = False
    satisfaction_good: bool = False
    satisfaction_regular: bool = False
    satisfaction_bad: bool = False
    opinions: str = ""
    causes: str = ""
    observations: str = ""
    causes_tags: List[Options] = []
    causes_others: str = ""
