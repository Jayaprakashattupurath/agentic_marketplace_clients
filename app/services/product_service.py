"""
Product service for database operations
"""
from typing import List, Optional
from app.database import get_database
from app.models.product import Product, ProductCreate, ProductInsight
from bson import ObjectId
from datetime import datetime


class ProductService:
    """Service for product database operations"""
    
    @staticmethod
    async def create_product(product: ProductCreate) -> Product:
        """Create a new product"""
        db = get_database()
        product_dict = product.model_dump()
        product_dict["created_at"] = datetime.utcnow()
        product_dict["updated_at"] = datetime.utcnow()
        
        result = await db.products.insert_one(product_dict)
        created_product = await db.products.find_one({"_id": result.inserted_id})
        return Product(**created_product)
    
    @staticmethod
    async def get_product(product_id: str) -> Optional[Product]:
        """Get a product by ID"""
        db = get_database()
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        if product:
            return Product(**product)
        return None
    
    @staticmethod
    async def get_products(
        skip: int = 0,
        limit: int = 100,
        marketplace: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Product]:
        """Get products with optional filters"""
        db = get_database()
        query = {}
        
        if marketplace:
            query["marketplace"] = marketplace
        if category:
            query["category"] = category
        
        cursor = db.products.find(query).skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        return [Product(**product) for product in products]
    
    @staticmethod
    async def update_product(product_id: str, product_update: dict) -> Optional[Product]:
        """Update a product"""
        db = get_database()
        product_update["updated_at"] = datetime.utcnow()
        
        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product_update}
        )
        
        if result.modified_count:
            updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
            return Product(**updated_product)
        return None
    
    @staticmethod
    async def delete_product(product_id: str) -> bool:
        """Delete a product"""
        db = get_database()
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
    
    @staticmethod
    async def save_insight(insight: ProductInsight) -> dict:
        """Save a product insight"""
        db = get_database()
        insight_dict = insight.model_dump()
        result = await db.insights.insert_one(insight_dict)
        return {"id": str(result.inserted_id), **insight_dict}
    
    @staticmethod
    async def get_product_insights(product_id: str) -> List[dict]:
        """Get all insights for a product"""
        db = get_database()
        cursor = db.insights.find({"product_id": product_id}).sort("generated_at", -1)
        insights = await cursor.to_list(length=100)
        return insights


product_service = ProductService()

