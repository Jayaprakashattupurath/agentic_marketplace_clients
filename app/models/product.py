"""
Product data models
"""
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, List, Dict, Any, Annotated
from datetime import datetime
from bson import ObjectId


def validate_object_id(v: Any) -> str:
    """Validate and convert ObjectId to string"""
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId string")
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]


class ProductBase(BaseModel):
    """Base product model"""
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    marketplace: str
    product_id: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ProductCreate(ProductBase):
    """Product creation model"""
    pass


class Product(ProductBase):
    """Product model with ID"""
    id: Optional[PyObjectId] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        str_strip_whitespace=True
    )


class ProductInsight(BaseModel):
    """Product insight model"""
    product_id: str
    insight_type: str  # e.g., "trend_analysis", "competitor_analysis", "pricing_insight"
    insight_content: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class InsightRequest(BaseModel):
    """Request model for generating insights"""
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    insight_type: str = "general"
    context: Optional[str] = None
    include_competitors: bool = False

