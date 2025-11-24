"""
API routes for product management
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.product import Product, ProductCreate
from app.services.product_service import product_service

router = APIRouter()


@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    """
    Create a new product
    """
    try:
        created_product = await product_service.create_product(product)
        return created_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")


@router.get("/products", response_model=List[Product])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    marketplace: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Get list of products with optional filters
    """
    try:
        products = await product_service.get_products(
            skip=skip,
            limit=limit,
            marketplace=marketplace,
            category=category
        )
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """
    Get a specific product by ID
    """
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_update: dict):
    """
    Update a product
    """
    updated_product = await product_service.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    """
    Delete a product
    """
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "message": "Product deleted successfully"}

