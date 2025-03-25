import yfinance as yf
from typing import Dict, Any
from datetime import datetime
from .news_service import get_stock_news

def get_stock_data(ticker: str) -> Dict[str, Any]:
    """
    Get basic stock information using yfinance
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Ensure we have the minimum required data
        if not info:
            raise Exception(f"No data found for ticker {ticker}")
            
        # Create performance dict with default values
        performance = {
            "day_change": info.get("regularMarketChangePercent", 0),
            "year_high": info.get("fiftyTwoWeekHigh", 0),
            "year_low": info.get("fiftyTwoWeekLow", 0)
        }

        # Convert timestamp to date string if it exists
        dividend_date = info.get("lastDividendDate")
        if dividend_date:
            dividend_date = datetime.fromtimestamp(dividend_date).strftime("%Y-%m-%d")

        # Get dividend information
        dividend_info = {
            "pays_dividend": info.get("dividendRate", 0) > 0,
            "dividend_yield": info.get("dividendYield", 0),
            "annual_dividend_rate": info.get("dividendRate", 0),
            "last_dividend_date": dividend_date
        }

        # Get company name for news search
        company_name = info.get("longName", "")
        
        # Get news data
        news_items = get_stock_news(ticker, company_name)
        
        return {
            "ticker": ticker.upper(),
            "current_price": info.get("currentPrice", 0),
            "company_name": company_name,
            "currency": info.get("currency", "USD"),
            "sector": info.get("sector", "Unknown"),
            "performance": performance,
            "dividend_info": dividend_info,
            "news": news_items
        }
    except Exception as e:
        raise Exception(f"Error fetching stock data: {str(e)}")
