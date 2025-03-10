from pydantic import BaseModel
from typing import Optional, List

class StockPerformance(BaseModel):
    day_change: Optional[float] = None
    year_high: Optional[float] = None
    year_low: Optional[float] = None

class DividendInfo(BaseModel):
    pays_dividend: bool = False
    dividend_yield: Optional[float] = None
    annual_dividend_rate: Optional[float] = None
    last_dividend_date: Optional[str] = None

class NewsItem(BaseModel):
    title: str
    link: str
    published: str

class StockResponse(BaseModel):
    ticker: str
    current_price: Optional[float] = None
    company_name: Optional[str] = None
    currency: Optional[str] = None
    performance: StockPerformance
    dividend_info: DividendInfo
    news: List[NewsItem] = []
