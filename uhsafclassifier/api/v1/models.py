from datetime import datetime
from enum import Enum
from typing import List, Optional

from odmantic import Model


class Options(str, Enum):
    causes_deceased = "causes_deceased"
    causes_no_dir = "causes_no_dir"
    causes_quantity = "causes_quantity"
    causes_distance = "causes_distance"
    causes_low_quality = "causes_low_quality"
    causes_price = "causes_price"


class PersonModel(Model):
    date: Optional[datetime] = None
    municipality: Optional[str] = None
    saf: Optional[str] = None
    full_name: str
    ci: Optional[str] = None
    direction: Optional[str] = None
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
    opinions: Optional[str] = None
    causes: Optional[str] = None
    observations: Optional[str] = None
    causes_tags: List[Options] = []
    causes_others: Optional[str] = None
