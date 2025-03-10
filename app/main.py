from fastapi import FastAPI, HTTPException
from app.services.stock_service import get_stock_data
from app.models.schemas import StockResponse

app = FastAPI(
    title="Stock API",
    description="API for getting stock data and news",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Stock API is running!"}

@app.get("/stock/{ticker}", response_model=StockResponse)
async def get_stock(ticker: str):
    """Get stock data and news for a given ticker"""
    try:
        stock_data = get_stock_data(ticker)
        return stock_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))