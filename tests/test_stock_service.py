import pytest
from unittest.mock import patch, MagicMock
from app.services.stock_service import get_stock_data

@pytest.fixture
def mock_yf_ticker():
    with patch('yfinance.Ticker') as mock_ticker:
        # Create a mock stock info
        mock_info = {
            "currentPrice": 150.0,
            "longName": "Test Company",
            "currency": "USD",
            "sector": "Technology",
            "regularMarketChangePercent": 1.5,
            "fiftyTwoWeekHigh": 200.0,
            "fiftyTwoWeekLow": 100.0,
            "dividendRate": 0.88,
            "dividendYield": 0.02,
            "lastDividendDate": None
        }
        
        # Set up the mock ticker instance
        mock_instance = MagicMock()
        mock_instance.info = mock_info
        mock_ticker.return_value = mock_instance
        yield mock_ticker

def test_get_stock_data_sector(mock_yf_ticker):
    """Test that get_stock_data correctly handles the sector field"""
    # Test with sector present
    result = get_stock_data("AAPL")
    assert "sector" in result
    assert result["sector"] == "Technology"
    
    # Test with missing sector
    mock_yf_ticker.return_value.info = {
        "currentPrice": 150.0,
        "longName": "Test Company",
        # sector field intentionally omitted
    }
    result = get_stock_data("AAPL")
    assert "sector" in result
    assert result["sector"] == "Unknown"  # Should use default value

def test_get_stock_data_complete_response(mock_yf_ticker):
    """Test the complete response structure from get_stock_data"""
    result = get_stock_data("AAPL")
    
    # Check all expected fields are present
    assert isinstance(result, dict)
    assert all(key in result for key in [
        "ticker",
        "current_price",
        "company_name",
        "currency",
        "sector",
        "performance",
        "dividend_info",
        "news"
    ])
    
    # Verify specific field values
    assert result["ticker"] == "AAPL"
    assert result["sector"] == "Technology"
    assert result["currency"] == "USD"
    
    # Check nested structures
    assert isinstance(result["performance"], dict)
    assert isinstance(result["dividend_info"], dict)
    assert isinstance(result["news"], list) 