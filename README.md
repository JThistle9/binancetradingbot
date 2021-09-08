# Disclaimer

This is a personal, passion project of mine just for fun. It's not completed, currently only runs test orders, and I've never used this bot to lose or earn real money. Use at your own risk.

# Binance Trading Bot

This trading bot utilizes a strategy to analyze buy and sell signals for a set of cryptos and make trades on Binance.
The intentions were for this bot to be ran on minute intervals or slower, so the apis used have not been aggressively scrutizined for speed nor will the strategies look for extremely small, buy-and-sell opportunities within seconds.

Next section is project structure. If you just want to run the trading bot, skip to [Setup section](#Setup).

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

# Setup

First run `pip install -r requirements.txt` to install necessary dependencies.

## Quick Start w/ Default Implementation
Simply run `python3 run.py` or `python3 -m run` inside src folder to run default implementation with AvgStategy.

## Learn More
Try out `python3 run.py -h` or `python3 -m run -h` to learn more about specifications that can be provided! See current help output below:

	usage: run.py [-h] [-s STRATEGY] [-c CONFIG] [-hi {1m,5m,1h,1d}]
	              [-hw HISTORICAL_WINDOW] [-tp TAKE_PROFIT]
	optional arguments:
	  -h, --help            show this help message and exit
	  -s STRATEGY, --strategy STRATEGY
	                        strategy used by the trading bot. Default: AvgStrategy
	  -c CONFIG, --config CONFIG
	                        dictionary of configurations for the specified
	                        strategy. Default: to {"sellPercent":"0.02",
	                        "buyPercent":"0.02", "slope_num_intervals":"3"}
	  -hi {1m,5m,1h,1d}, --historical-interval {1m,5m,1h,1d}
	                        interval of historical data, i.e. the frequency of
	                        datapoints. Default: 5m
	  -hw HISTORICAL_WINDOW, --historical-window HISTORICAL_WINDOW
	                        window of historical data in days, i.e. the X latest
	                        days of data. Default: 30
	  -tp TAKE_PROFIT, --take-profit TAKE_PROFIT
	                        The take profit percent that must have been made
	                        before a crypto will be sellable. Default: 0.01

## Customize & Grow!
What's especially great about this trading bot is that the main logic in run.py is strategy agnostic, so we can try out all sorts of different strategies defined in a Strategy class under the src/strategies/ folder.

Create a new strategy class that defines sell and buy signals; use AvgStrategy.py as an example. From there run the trading bot specifying your strategy class & config json if necessary.

If you're not sure where to start but would like to help out, EMAStrategy.py is not completed and could use some love. Research Exponential Moving Average (EMA) golden cross and death cross and implement a stategy class that determines buy and sell signals using those crosses.