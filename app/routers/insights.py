"""
API routes for product insights
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.models.product import InsightRequest, ProductInsight
from app.services.ollama_service import ollama_service
from app.services.product_service import product_service
from app.database import get_database
from datetime import datetime

router = APIRouter()


@router.post("/insights/generate")
async def generate_insight(request: InsightRequest):
    """
    Generate AI-powered insights for a product
    """
    try:
        # Get product information if product_id is provided
        product = None
        if request.product_id:
            product = await product_service.get_product(request.product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
        
        # Generate insight using Ollama
        insight_data = await ollama_service.generate_product_insight(
            product_name=request.product_name or (product.name if product else "Unknown Product"),
            product_description=product.description if product else None,
            category=product.category if product else None,
            price=product.price if product else None,
            marketplace=product.marketplace if product else None,
            insight_type=request.insight_type,
            context=request.context
        )
        
        # Save insight to database if product_id is provided
        if request.product_id:
            insight = ProductInsight(
                product_id=request.product_id,
                insight_type=insight_data["insight_type"],
                insight_content=insight_data["insight_content"],
                generated_at=datetime.utcnow(),
                metadata=insight_data.get("metadata")
            )
            await product_service.save_insight(insight)
        
        return {
            "success": True,
            "insight": insight_data,
            "product_id": request.product_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insight: {str(e)}")


@router.get("/insights/product/{product_id}")
async def get_product_insights(product_id: str):
    """
    Get all insights for a specific product
    """
    try:
        insights = await product_service.get_product_insights(product_id)
        return {
            "success": True,
            "product_id": product_id,
            "insights": insights,
            "count": len(insights)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching insights: {str(e)}")


@router.post("/insights/compare")
async def compare_products(products: list):
    """
    Compare multiple products and generate comparative insights
    """
    try:
        if len(products) < 2:
            raise HTTPException(status_code=400, detail="At least 2 products required for comparison")
        
        comparison = await ollama_service.compare_products(products)
        
        return {
            "success": True,
            "comparison": comparison,
            "products_count": len(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing products: {str(e)}")


@router.get("/insights/models")
async def list_ollama_models():
    """
    List available Ollama models
    """
    try:
        models = await ollama_service.list_available_models()
        return {
            "success": True,
            "models": models,
            "current_model": ollama_service.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

