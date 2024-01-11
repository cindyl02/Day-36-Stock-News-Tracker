import requests
import datetime as dt
import html
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stocks_list = [("TSLA", "Tesla")]
today = str(dt.datetime.now()).split(" ")[0]

for (stock, company_name) in stocks_list:
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "apikey": STOCK_API_KEY,
    }
    news_params = {
        "qInTitle": company_name,
        "from": today,
        "to": today,
        "sortBy": "relevancy",
        "apiKey": NEWS_API_KEY,
        "pageSize": 3,
        "language": "en",
    }
    response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    data_list = [stock_price_dict for (_, stock_price_dict) in data.items()]

    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]

    day_before_yesterday_data = data_list[1]
    day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

    difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
    print(f"difference is {difference}")
    diff_percent = round((difference / float(yesterday_closing_price)) * 100)
    print(f"difference percent is {diff_percent}")

    if diff_percent > 5:
        response = requests.get(url=NEWS_ENDPOINT, params=news_params)
        response.raise_for_status()
        articles = response.json()["articles"]
        print(articles)
        for article in articles:
            if diff_percent > 0:
                up_down = "🔺"
            else:
                up_down = "🔻"
            content = f"{stock}: {up_down}{diff_percent}%\nHeadline: {html.unescape(article["title"])}\n Brief: {html.unescape(article["description"])}"
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=content
                )
