## Stock News Tracker
### About
This project uses AlphaVantage API and News API and SMTP to send an email to the provided email address in `main.py` whenever the stock goes up or down by more than 5%.

### How to setup
1. Create a AlphaVantage account and update STOCK_API_KEY. 
2. Create a News API account and update NEWS_API_KEY.
3. Run main.py and look for an email if the stock has gone up or down by more than 5% between yesterday and the day before yesterday closing price. 
