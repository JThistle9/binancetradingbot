# Disclaimer

This is a personal, passion project of mine just for fun. It's not completed, currently only runs test orders, and I've never used this bot to lose or earn real money. Use at your own risk.

# Binance Trading Bot

This trading bot utilizes a strategy to analyze buy and sell signals for a set of cryptos and make trades on Binance.
The intentions were for this bot to be ran on minute intervals or slower, so the apis used have not been aggressively scrutizined for speed nor will the strategies look for extremely small, buy-and-sell opportunities within seconds.

## Project Structure

run.py: the main method for running the trading bot

run_trading_bot.sh: shell script ran by a cron job on my raspberry pi to run the trading bot once a minute.

### Credentials Folder

Stores binance and spreadsheet credentials. This folder is empty on GitHub because no one should see anyone's credentials. If you do intend on committing to this repo, please do not include any credentials.

### Helpers Folder

Stores python files of various helper methods. This is the nitty-gritty logic that's abstracted away so that the main run.py file looks clean and easy to understand.

 - **trading_bot_helpers.py**: the general helper methods for run.py and strategy classes

 - **init.py**: the methods for initializing the trading bot

 - **historical_data.py**: the methods for retrieving crypto price histories

 - **spreadsheet_snippets.py**: the class used for retrieving and storing spreadsheet data

 - **project_paths.py**: contains relative paths to folders in this project

### Stategies

Stores python classes for the strategies that can be utilized by the trading bot. The main run.py is given a stategy and calls strategy.buySingal and strategy.sellSignal to determine if it's the time to buy or sell a crypto. This abstraction allows easy scalability to any number of strategies that can be run/tested by the bot.

 - **AvgStrategy**: provides a buy or sell signal based on historical price average. If below the average price by X%, buy. If above the average price by Y%, sell.

 - **EMAStrategy [INCOMPLETE]**: provides a buy or sell signal based on crypto's X-day and Y-day Expotential Moving Averages. If golden cross, buy. If death cross, sell.
