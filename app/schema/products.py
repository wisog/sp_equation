from datetime import datetime, timedelta, timezone
from email import utils as email_utils
from typing import Optional, Any, TypedDict, List

from pydantic import BaseModel, constr, confloat, PositiveInt, validator, conset

# Minimal expiration time, 30 days with 5 second as precision
MINIMAL_EXPIRATION = timedelta(days=30) - timedelta(seconds=5)

Name = constr(max_length=50)
Rating = confloat(ge=0, le=10)
CategoryID = int
BrandID = int


class ProductUpdateRequest(BaseModel):
    """
    Defines schema and validation for update request.
    """
    name: Optional[Name]
    rating: Optional[Rating]
    featured: Optional[bool]

    receipt_date: Optional[datetime]
    expiration_date: Optional[datetime]

    brand: Optional[BrandID]
    categories: Optional[conset(CategoryID, min_items=1, max_items=5)]

    items_in_stock: Optional[PositiveInt]

    @validator("receipt_date", "expiration_date", pre=True)
    def parse_rfc_1123_datetime(cls, date: Any):
        """
        Parse string value as date in RFC 1123 format.
        @param date: date with unknown type, will be processed if string. Otherwise validator is skipped.
        @return: datetime object or string (if unable to parse as RFC 1123 formatted string)
        """
        if isinstance(date, str):
            parsed_datetime = email_utils.parsedate_to_datetime(date)
            if parsed_datetime is None:
                return date
            return parsed_datetime
        return date


class ProductCreateRequest(ProductUpdateRequest):
    """
    Defines schema and validation for creation request.
    Mostly makes some fields required.
    """
    name: Name
    rating: Rating
    featured: Optional[bool]
    receipt_date: Optional[datetime]
    expiration_date: Optional[datetime]

    brand: BrandID
    categories: conset(CategoryID, min_items=1, max_items=5)

    items_in_stock: PositiveInt

    @validator('expiration_date')
    def expires_in_more_30_days(cls, date: Any):
        """
        Check date in the future that the difference from now is at least 30 days.
        @param date: datetime
        @return: datetime object
        """
        now = datetime.now(timezone.utc)
        diff = date - now
        if diff.days < 30:
            raise ValueError('Expiration date should be at least 30 days in the future')

        return date


class BrandPresentation(TypedDict):
    """
    Describes Brand resource presentation.
    """
    id: int
    name: str
    country_code: str


class CategoryPresentation(TypedDict):
    """
    Describes Category resource presentation.
    """
    id: int
    name: str


class ProductPresentation(TypedDict):
    """
    Describes Product resource presentation
    """
    id: int
    name: str
    rating: int
    featured: bool
    items_in_stock: int
    receipt_date: datetime
    brand: BrandPresentation
    categories: List[CategoryPresentation]
    expiration_date: datetime
    created_at: datetime
