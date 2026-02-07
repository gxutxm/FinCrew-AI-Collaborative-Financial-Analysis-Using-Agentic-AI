"""
MARKET RESEARCH AGENT
======================
Fetches financial news and analyzes sentiment.

Original notebook by: Student 1
Converted to module by: GG
"""

import requests
import os
import re
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

# Load API key
load_dotenv()
finnhub_key = os.getenv("FINNHUB_API_KEY")

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    """Clean and normalize text."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"[^\w\s.,?!]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def get_sentiment_vader(text):
    """Classify sentiment using VADER."""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return "Bullish", compound
    elif compound <= -0.05:
        return "Bearish", compound
    else:
        return "Neutral", compound


def extract_keywords(news_list):
    """Extract top keywords from headlines."""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'has', 'have'}
    all_words = []
    for item in news_list:
        words = re.findall(r'\b[a-z]{4,}\b', item['title'].lower())
        all_words.extend([w for w in words if w not in stop_words])
    return Counter(all_words).most_common(10)

def fetch_news(ticker, from_date, to_date):
    """Fetch news headlines from Finnhub."""
    if not finnhub_key:
        return [], "Missing FINNHUB_API_KEY in .env file"
    
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={from_date}&to={to_date}&token={finnhub_key}"
    
    try:
        data = requests.get(url).json()
    except Exception as e:
        return [], f"Error fetching news: {e}"
    
    headlines = []
    for item in data[:10]:
        title = clean_text(item.get("headline", ""))
        link = item.get("url", "")
        if title:
            headlines.append({"title": title, "link": link})
    
    return headlines, None


def fetch_earnings(ticker):
    """Fetch latest earnings data from Finnhub."""
    if not finnhub_key:
        return None
    
    url = f"https://finnhub.io/api/v1/stock/earnings?symbol={ticker}&token={finnhub_key}"
    
    try:
        data = requests.get(url).json()
        if data and len(data) > 0:
            latest = data[0]
            return {
                "actual_eps": latest.get("actual"),
                "estimated_eps": latest.get("estimate"),
                "surprise_percent": latest.get("surprisePercent"),
                "reported_date": latest.get("period")
            }
    except Exception:
        pass
    
    return None


def analyze_market(ticker, from_date, to_date):
    """
    Main function to analyze market sentiment for a stock.
    
    Parameters:
        ticker: Stock symbol (e.g., 'AAPL')
        from_date: Start date 'YYYY-MM-DD'
        to_date: End date 'YYYY-MM-DD'
    
    Returns:
        dict with sentiment analysis results
    """
    # Fetch news
    news, error = fetch_news(ticker, from_date, to_date)
    
    if error:
        return {"success": False, "error": error}
    
    if not news:
        return {"success": False, "error": "No news found for this ticker/date range"}
    
    # Analyze sentiment for each headline
    sentiments = []
    compound_scores = []
    
    for item in news:
        sentiment, score = get_sentiment_vader(item['title'])
        sentiments.append(sentiment)
        compound_scores.append(score)
    
    # Count sentiments
    bullish = sentiments.count('Bullish')
    bearish = sentiments.count('Bearish')
    neutral = sentiments.count('Neutral')
    total = len(news)
    
    # Overall signal
    if bullish > bearish:
        overall_signal = "Bullish"
    elif bearish > bullish:
        overall_signal = "Bearish"
    else:
        overall_signal = "Neutral"
    
    # Confidence score (average of absolute compound scores)
    avg_compound = sum(compound_scores) / len(compound_scores)
    confidence = round(abs(avg_compound) + 0.5 * (max(bullish, bearish) / total), 2)
    confidence = min(confidence, 1.0)  # Cap at 1.0
    
    # Extract keywords
    top_keywords = extract_keywords(news)
    
    # Identify risks (bearish headlines)
    key_risks = [item['title'] for item, sent in zip(news, sentiments) if sent == 'Bearish'][:3]
    if not key_risks:
        key_risks = ["No significant risks identified"]
    
    # Summary points (bullish headlines)
    summary_points = [item['title'] for item, sent in zip(news, sentiments) if sent == 'Bullish'][:3]
    if not summary_points:
        summary_points = [f"Analyzed {total} headlines", f"Overall sentiment: {overall_signal}"]
    
    # Fetch earnings
    earnings = fetch_earnings(ticker)
    
    return {
        "success": True,
        "ticker": ticker,
        "period": {"from": from_date, "to": to_date},
        "headlines_analyzed": total,
        "sentiment_counts": {
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral
        },
        "overall_signal": overall_signal,
        "confidence_score": confidence,
        "top_keywords": [word for word, count in top_keywords[:5]],
        "key_risks": key_risks,
        "summary": summary_points,
        "earnings": earnings
    }

def to_report_format(result):
    """
    Convert output to Report Writer's expected schema.
    """
    if not result['success']:
        return {"market_research": {}, "error": result.get('error')}
    
    return {
        "market_research": {
            "sentiment": result["overall_signal"],
            "confidence_score": result["confidence_score"],
            "key_risks": result["key_risks"],
            "summary": result["summary"]
        }
    }


if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("MARKET RESEARCH AGENT TEST")
    print("=" * 60)
    
    # Test with AAPL
    ticker = "AAPL"
    from_date = "2026-02-01"
    to_date = "2026-02-06"
    
    print(f"\nAnalyzing {ticker} from {from_date} to {to_date}...")
    
    result = analyze_market(ticker, from_date, to_date)
    
    if result['success']:
        print(f"\nSuccess!")
        print(f"Headlines analyzed: {result['headlines_analyzed']}")
        print(f"Overall signal: {result['overall_signal']}")
        print(f"Confidence: {result['confidence_score']}")
        print(f"Top keywords: {result['top_keywords']}")
        
        print("\n--- Report Writer Format ---")
        report_format = to_report_format(result)
        print(json.dumps(report_format, indent=2))
    else:
        print(f"\nFailed: {result['error']}")