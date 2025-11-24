"""
Product data models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


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

