# Weather Check Agent

Weather Check Agent is a lightweight automation tool built with Python and Selenium that automates a daily task—retrieving the current weather for a specified city. Instead of manually checking the weather online, this agent opens Google’s weather search page, extracts the current weather condition, and compares it with an expected condition provided by the user.

## Problem Statement

Many users perform daily weather checks manually to plan their day. Weather Check Agent automates this routine by:
- Accepting a city name (e.g., "New York") and an expected weather condition (e.g., "Sunny") as input.
- Navigating to Google’s weather search results for that city.
- Extracting the current weather condition from the page.
- Comparing the actual weather condition with the expected condition and outputting whether they match.

This simple automation reduces manual effort and provides a quick way to verify weather conditions each day.

## Features

- **Automated Weather Retrieval:** Opens a browser and fetches the current weather for a given city.
- **Validation:** Compares the extracted weather condition with the expected condition.
- **Command-Line Interface:** Run the script with a single command.
- **Simple & Extendable:** A basic framework that can be adapted for other browser automation tasks.

## Requirements

- **Python 3.x**
- **Selenium:** Install using pip:
  ```bash
  pip install selenium

WebDriver:
For Chrome, download ChromeDriver.
For Firefox, download GeckoDriver.
Note: With Selenium 4.6+, Selenium Manager can automatically manage drivers.

**Installation**
1. Clone the Repository:
```bash
git clone https://github.com/your-username/weather-check-agent.git
cd weather-check-agent
```
2. 
