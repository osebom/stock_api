import pytest
from app.services.stock_service import get_stock_data
from app.services.news_service import get_stock_news

def test_stock_data_structure():
    """Check if stock data has everything we need"""
    data = get_stock_data("AAPL")
    
    # Basic Quality Check
    assert data["ticker"] == "AAPL"
    assert data["current_price"] > 0
    assert data["company_name"]
    
    # Performance Check
    assert "day_change" in data["performance"]
    assert "year_high" in data["performance"]
    assert "year_low" in data["performance"]
    
    # Dividend Check
    assert "dividend_info" in data
    assert isinstance(data["dividend_info"]["pays_dividend"], bool)
    
    # News Check
    assert "news" in data
    assert isinstance(data["news"], list)
    assert len(data["news"]) <= 3

def test_invalid_stock():
    """Check how we handle bad stock symbols"""
    with pytest.raises(Exception):
        get_stock_data("NOTREAL")

def test_news_data():
    """Check if news fetching works"""
    news = get_stock_news("AAPL", "Apple Inc")
    assert len(news) <= 3
    if news:
        first_news = news[0]
        assert "title" in first_news
        assert "link" in first_news
        assert "published" in first_news