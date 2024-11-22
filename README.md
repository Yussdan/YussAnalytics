# Crypto Analytics Bot

Crypto Analytics Bot is a Telegram bot that provides cryptocurrency analytics and visualizations. The bot interacts with an API to fetch live cryptocurrency prices, historical data, and generates analytics and visualizations. It also stores and retrieves visualization images from AWS S3 for efficiency.

---

## Features

- **Live Prices**: Get the latest exchange rate of popular cryptocurrencies.
- **Historical Data**: Analyze historical data over the past 10 hours or 10 days
- **Analytics**:
  - Average, median, minimum, and maximum prices.
- **Visualizations**:
  - Line plots with percentage changes highlighted in red/green.
  - Images are stored in AWS S3 for quick retrieval.
- **Interactive Telegram Menu**:
  - Select cryptocurrency and analytics period using buttons.

---

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: Telegram Bot API
- **Data Analysis**: Pandas
- **Visualization**: Matplotlib
- **Cloud Storage**: AWS S3
- **Environment Management**: dotenv

