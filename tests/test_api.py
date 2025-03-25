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
    
    # Define core required fields and their expected types
    required_fields = {
        "ticker": str,
        "current_price": (int, float),
        "company_name": str,
        "news": list
    }
    
    # Check that all required fields are present and of correct type
    for field, expected_type in required_fields.items():
        assert field in data, f"Required field '{field}' is missing"
        assert isinstance(data[field], expected_type), f"Field '{field}' has wrong type"
    
    # Check nested structures maintain their required format
    assert "performance" in data
    performance = data["performance"]
    assert all(key in performance for key in ["day_change", "year_high", "year_low"])
    
    assert "dividend_info" in data
    dividend_info = data["dividend_info"]
    assert all(key in dividend_info for key in ["pays_dividend", "dividend_yield", "annual_dividend_rate", "last_dividend_date"])

    # Additional fields are allowed without breaking the test
    # No need to modify this test when adding new top-level fields

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
