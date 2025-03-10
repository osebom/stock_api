import feedparser
from typing import List, Dict, Any
from urllib.parse import quote

def get_stock_news(ticker: str, company_name: str) -> List[Dict[str, Any]]:
    """
    Get news for a stock using Google News RSS feed
    """
    try:
        # Create search query using ticker and company name
        search_query = f"{ticker} {company_name}"
        
        # Create the Google News URL with search query
        base_url = 'https://news.google.com/rss/search?q='
        url = f"{base_url}{quote(search_query)}&hl=en-US&gl=US&ceid=US:en"
        
        # Parse the RSS feed
        feed = feedparser.parse(url)
        
        # Get all items and prepare news list
        news_items = []
        for newsitem in feed['items']:
            news_items.append({
                'title': newsitem.get('title', ''),
                'link': newsitem.get('link', ''),
                'published': newsitem.get('published', ''),
                'published_parsed': newsitem.get('published_parsed', None)  # For sorting
            })
        
        # Sort by date (most recent first) and get top 3
        news_items.sort(key=lambda x: x['published_parsed'] or (0,), reverse=True)
        
        # Return only the fields we want in the API
        return [{
            'title': item['title'],
            'link': item['link'],
            'published': item['published']
        } for item in news_items[:3]]

    except Exception as e:
        raise Exception(f"Error fetching news: {str(e)}")
