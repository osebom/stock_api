import feedparser
from urllib.parse import quote  # For encoding the search query
from datetime import datetime  # For parsing dates

# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines( rss_url, search_query=None ):
    headlines = []
    
    feed = parseRSS( rss_url )
    # Get all items first
    for newsitem in feed['items']:
        # If search query is provided, only include matching items
        if search_query:
            if search_query.lower() not in newsitem.get('title', '').lower():
                continue
                
        headlines.append({
            'title': newsitem.get('title', ''),
            'link': newsitem.get('link', ''),
            'published': newsitem.get('published', ''),
            'content': newsitem.get('summary_detail', ''),
            'published_parsed': newsitem.get('published_parsed', None)  # For sorting
        })
    
    # Sort by date (most recent first) and get top 3
    headlines.sort(key=lambda x: x['published_parsed'] or (0,), reverse=True)
    return headlines[:3]

# A list to hold all headlines
allheadlines = []

# Search query
search_query = "NVIDIA"  # You can change this to any stock/company name

# Create the Google News URL with search query
base_url = 'https://news.google.com/rss/search?q='
newsurls = {
    'googlenews': f"{base_url}{quote(search_query)}&hl=en-US&gl=US&ceid=US:en",
}

# Iterate over the feed urls
for key, url in newsurls.items():
    print(f"\nGetting 3 most recent news for '{search_query}' from {key}:")
    headlines = getHeadlines(url)
    allheadlines.extend(headlines)
    
    # Print the headlines with more detail
    for item in headlines:
        print(f"\nTitle: {item['title']}")
        print(f"Published: {item['published']}")
        print(f"Link: {item['link']}")
        print("-" * 80)

# # Iterate over the allheadlines list and print each headline
# for hl in allheadlines:
#     print(hl)
 