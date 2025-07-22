import requests
import re
import dateparser
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import math
import google.generativeai as genai
import os
from langchain.tools import tool



NEWS_API_KEY = "news_api"
def get_all_tech_news(user_message, max_pages=3):
    try:
        lower_msg = user_message.lower()
        if "today" in lower_msg or "for the day" in lower_msg:
            parsed_date = datetime.now()
        elif "yesterday" in lower_msg:
            parsed_date = datetime.now() - timedelta(days=1)
        else:
            parsed_date = dateparser.parse(user_message)
        if not parsed_date:
            parsed_date = datetime.now()
    except Exception:
        parsed_date = datetime.now()

    date_from = parsed_date.strftime('%Y-%m-%d')
    headlines = []
    page = 1
    while page <= max_pages:
        url = (
            f"https://newsapi.org/v2/everything?q=technology&from={date_from}"
            f"&sortBy=publishedAt&pageSize=100&page={page}&apiKey={NEWS_API_KEY}"
        )
        try:
            res = requests.get(url)
            res.raise_for_status()
            articles = res.json().get("articles", [])
            if not articles:
                break
            for article in articles:
                title = article.get("title", "[No Title]")
                source = article.get("source", {}).get("name", "Unknown")
                url = article.get("url", "")
                headlines.append(f"{len(headlines)+1}. {title} ({source})\n{url}")
                if len(headlines) >= 10:
                    break
            if len(headlines) >= 10:
                break
            page += 1

        except requests.exceptions.RequestException as e:
            return f" API Error: {e}"
        except Exception as e:
            return f" Unexpected Error: {e}"

    if not headlines:
        return f"No tech news found for {date_from}."

    return "\n\n".join(headlines)




genai.configure(api_key=os.getenv("API_key"))
def code_helper(code: str, model_name: str = "gemini-1.5-pro"):
    prompt = f"""You are an expert coding tutor. Explain what the following code does, step by step, in a clear and easy-to-understand way:\n\n```python\n{code}\n```"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f" Error while using Gemini: {str(e)}"




def get_stock_price(query):
    try:
        company = (
            query.lower()
            .replace("stock price of", "")
            .replace("stock price", "")
            .replace("what is", "")
            .replace("?", "")
            .strip()
        ).title()
        headers = {"User-Agent": "Mozilla/5.0"}

        search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company}"
        search_res = requests.get(search_url, headers=headers, timeout=10)
        search_data = search_res.json()
        if not search_data.get("quotes"):
            return None
        symbol = search_data["quotes"][0]["symbol"]
        quote_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        quote_res = requests.get(quote_url, headers=headers, timeout=10)
        quote_data = quote_res.json()
        price = quote_data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return price
    except:
        return None


WEATHER_API_KEY = "weather_api"
def extract_city_from_text(text):
    match = re.search(r"in\s+([a-zA-Z\s]+)", text.lower())
    if match:
        return match.group(1).strip()
    return text.strip()
def get_weather(text):
    try:
        city = extract_city_from_text(text)
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if "error" in data:
            return f"Weather not found for {city.title()}. Error: {data['error'].get('message', 'Unknown error')}"

        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feelslike_c = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        return (
            f"Current weather in {city.title()}: {temp_c}°C (feels like {feelslike_c}°C), "
            f"{condition}. Humidity: {humidity}%"
        )
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


def calculate_expression(expr):
    try:
        expr = expr.lower()
        expr = expr.replace("what is", "").replace("calculate", "").strip()
        expr = expr.replace("times", "*").replace("multiplied by", "*")
        expr = expr.replace("plus", "+").replace("minus", "-").replace("divided by", "/")        
        allowed_chars = set("0123456789+-*/.() ")
        allowed_names = set(dir(math)) | {"__builtins__"}
        if not all(c in allowed_chars for c in expr.replace(" ", "")):
            return f"Invalid characters in expression: {expr}"
            
        result = eval(expr, {"__builtins__": {}}, math.__dict__)
        return f"Result: {result}"
    except Exception as e:
        return f"Invalid expression '{expr}': {str(e)}"



tool_map = {
    "tech_news": get_all_tech_news,
    "code_helper": code_helper,
    "stock_price": get_stock_price,
    "weather": get_weather,
    "calculator": calculate_expression
}

def invoke_tool(tool_name, query):
    tool_func = tool_map.get(tool_name)
    if tool_func:
        return tool_func(query)
    return "Tool not found."