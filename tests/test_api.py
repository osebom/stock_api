from fastapi.testclient import TestClient
from app.main import app
import pytest

# Create a test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Stock API is running!"}

def test_get_valid_stock():
    """Test getting data for a valid stock ticker"""
    response = client.get("/stock/AAPL")
    assert response.status_code == 200
    data = response.json()
    
    # Check structure of response
    assert "ticker" in data
    assert "current_price" in data
    assert "company_name" in data
    assert "performance" in data
    assert "dividend_info" in data
    assert "news" in data

    # Check data types
    assert isinstance(data["ticker"], str)
    assert isinstance(data["current_price"], (int, float))
    assert isinstance(data["news"], list)

def test_get_invalid_stock():
    """Test getting data for an invalid stock ticker"""
    response = client.get("/stock/INVALID")
    assert response.status_code == 404
    assert "detail" in response.json()

@pytest.mark.parametrize("ticker", ["AAPL", "MSFT", "GOOGL"])
def test_multiple_valid_stocks(ticker):
    """Test getting data for multiple valid stock tickers"""
    response = client.get(f"/stock/{ticker}")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == ticker

def test_stock_performance_data():
    """Test the performance data structure in stock response"""
    response = client.get("/stock/AAPL")
    assert response.status_code == 200
    data = response.json()
    
    # Check performance metrics
    performance = data["performance"]
    assert "day_change" in performance
    assert "year_high" in performance
    assert "year_low" in performance
    
    # Check data types
    assert isinstance(performance["day_change"], (int, float))
    assert isinstance(performance["year_high"], (int, float))
    assert isinstance(performance["year_low"], (int, float))

def test_stock_news_data():
    """Test the news data structure in stock response"""
    response = client.get("/stock/AAPL")
    assert response.status_code == 200
    data = response.json()
    
    # Check news data
    assert "news" in data
    news = data["news"]
    assert isinstance(news, list)
    assert len(news) <= 3  # Maximum 3 news items
    
    if len(news) > 0:
        first_news = news[0]
        assert "title" in first_news
        assert "link" in first_news
        assert "published" in first_news

def test_empty_ticker():
    """Test behavior with empty ticker"""
    response = client.get("/stock/")
    assert response.status_code == 404

def test_special_characters_ticker():
    """Test behavior with special characters in ticker"""
    response = client.get("/stock/$$$")
    assert response.status_code == 404
