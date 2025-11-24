"""
Ollama service for AI-powered insights generation
"""
import httpx
from typing import Optional, Dict, Any
from app.config import settings
import json


class OllamaService:
    """Service for interacting with Ollama API"""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    async def generate_insight(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate insight using Ollama
        
        Args:
            prompt: User prompt
            model: Model name (optional, uses default if not provided)
            system_prompt: System prompt for context (optional)
        
        Returns:
            Generated insight text
        """
        model = model or self.model
        
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": model,
                        "messages": messages,
                        "stream": False
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result.get("message", {}).get("content", "")
            except httpx.HTTPError as e:
                raise Exception(f"Error calling Ollama API: {str(e)}")
    
    async def generate_product_insight(
        self,
        product_name: str,
        product_description: Optional[str] = None,
        category: Optional[str] = None,
        price: Optional[float] = None,
        marketplace: Optional[str] = None,
        insight_type: str = "general",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate product-specific insights
        
        Args:
            product_name: Name of the product
            product_description: Product description
            category: Product category
            price: Product price
            marketplace: Marketplace name
            insight_type: Type of insight to generate
            context: Additional context
        
        Returns:
            Dictionary containing insight data
        """
        system_prompt = """You are an expert market analyst specializing in e-commerce and marketplace insights. 
        Your role is to provide actionable, data-driven insights about products in online marketplaces.
        Be concise, specific, and focus on actionable recommendations."""
        
        # Build context for the prompt
        context_parts = [f"Product: {product_name}"]
        
        if product_description:
            context_parts.append(f"Description: {product_description}")
        if category:
            context_parts.append(f"Category: {category}")
        if price:
            context_parts.append(f"Price: ${price:.2f}")
        if marketplace:
            context_parts.append(f"Marketplace: {marketplace}")
        if context:
            context_parts.append(f"Additional Context: {context}")
        
        context_text = "\n".join(context_parts)
        
        # Generate insight based on type
        if insight_type == "trend_analysis":
            prompt = f"""Analyze the following product and provide trend insights:
            
{context_text}

Please provide:
1. Current market trends for this product
2. Demand indicators
3. Seasonal patterns (if applicable)
4. Growth potential
5. Key recommendations"""
        
        elif insight_type == "pricing_insight":
            prompt = f"""Analyze the pricing strategy for this product:
            
{context_text}

Please provide:
1. Price competitiveness analysis
2. Optimal pricing recommendations
3. Price positioning in the market
4. Discount opportunities
5. Value proposition assessment"""
        
        elif insight_type == "competitor_analysis":
            prompt = f"""Analyze competitors for this product:
            
{context_text}

Please provide:
1. Competitive landscape overview
2. Key differentiators
3. Competitive advantages and disadvantages
4. Market positioning
5. Strategic recommendations"""
        
        else:  # general
            prompt = f"""Provide comprehensive insights about this product:
            
{context_text}

Please provide:
1. Market overview
2. Key strengths and opportunities
3. Potential challenges
4. Recommendations for success
5. Actionable next steps"""
        
        insight_content = await self.generate_insight(
            prompt=prompt,
            system_prompt=system_prompt
        )
        
        return {
            "insight_type": insight_type,
            "insight_content": insight_content,
            "product_name": product_name,
            "metadata": {
                "model_used": model,
                "category": category,
                "price": price,
                "marketplace": marketplace
            }
        }
    
    async def compare_products(
        self,
        products: list,
        comparison_aspects: Optional[list] = None
    ) -> str:
        """
        Compare multiple products
        
        Args:
            products: List of product dictionaries
            comparison_aspects: Aspects to compare (optional)
        
        Returns:
            Comparison analysis text
        """
        system_prompt = """You are an expert product comparison analyst. 
        Provide detailed, objective comparisons between products."""
        
        products_text = "\n\n".join([
            f"Product {i+1}:\n" + "\n".join([f"{k}: {v}" for k, v in product.items()])
            for i, product in enumerate(products)
        ])
        
        aspects = comparison_aspects or ["price", "features", "quality", "value"]
        aspects_text = ", ".join(aspects)
        
        prompt = f"""Compare the following products focusing on: {aspects_text}

{products_text}

Please provide:
1. Side-by-side comparison
2. Strengths and weaknesses of each product
3. Best value recommendation
4. Target audience for each product
5. Final recommendation"""
        
        return await self.generate_insight(
            prompt=prompt,
            system_prompt=system_prompt
        )
    
    async def list_available_models(self) -> list:
        """List available Ollama models"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                result = response.json()
                return [model["name"] for model in result.get("models", [])]
            except httpx.HTTPError as e:
                raise Exception(f"Error fetching Ollama models: {str(e)}")


# Singleton instance
ollama_service = OllamaService()

