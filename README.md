# 🚀 DevEventBot – A Discord Bot for Dev Events in Kolkata

DevEventBot is a Python-based Discord bot that scrapes developer events, hackathons, and meetups from Devfolio and posts them directly **to** your Discord server.

It’s smart enough to:

- ✅ Include **online events** from all regions.
- 📍 Only include **offline events** happening in **Kolkata, Bengal, or West Bengal**.
- 🗓️ Generate **Google Calendar links** for events.
- 🌐 Scrape dynamically rendered websites using **Selenium**.

## 📦 Tech Stack

| Feature                | Technology                        |
| ---------------------- | --------------------------------- |
| Bot Framework          | discord.py                        |
| Environment Management | python-dotenv                     |
| Web Scraping           | requests, BeautifulSoup, Selenium |
| Date Handling          | datetime, pytz                    |
| Utility Libraries      | urllib.parse, json                |
| Headless Browser       | ChromeDriver via Selenium         |

---

## 🔧 Setup Instructions

### 1. 🔑 Clone the repository

```bash
git clone https://github.com/Avilash2001/KolkataEventsBot
cd deveventbot
```

### 2. 📁 Create a `.env` file

Create a `.env` file in the root directory and add your Discord bot token:

```env
DISCORD_TOKEN=your-bot-token-here
```

### 3. 🐍 Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. 📦 Install ChromeDriver

Make sure ChromeDriver is installed and added to your system PATH.

- [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

Ensure the version of ChromeDriver matches your installed version of Chrome.

### 5. ▶️ Run the bot

```bash
python bot.py
```

---

## 🧠 Features Overview

- 🕸️ **Dynamic Scraping**: Scrapes modern JS-rendered websites using Selenium.
- 📍 **Location Filter**: Includes only relevant offline events based on location.
- 🔗 **Google Calendar Links**: Auto-generates links for users to add events directly.
- ⏱️ **Asynchronous Scheduling**: Uses asyncio to efficiently manage scraping intervals.

---

## 📁 Project Structure

```
deveventbot/
│
├── bot.py               # Main entry point for the bot
├── scraper.py           # Contains web scraping logic
├── .env                 # Environment variables (not tracked)
├── config.json          # Configuration file
├── requirements.txt     # Python dependencies
├── test.py              # Test script for the bot
└── README.md            # Project documentation
```

---

## 🤝 Contributing

Pull requests are welcome! If you’d like to contribute, please fork the repository and use a feature branch. Contributions should include proper linting, documentation, and testing.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## ✨ Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Selenium](https://www.selenium.dev/)
- [Devfolio](https://devfolio.co/)
  