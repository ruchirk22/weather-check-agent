"""
Weather Checker Agent

This script automates checking the weather for a specified city and validates if it matches
an expected condition. It uses Selenium to navigate to Google Weather, extract the current
weather condition, and compare it with the expected condition.

Usage:
    python weather_checker.py <city_name> <expected_condition>

Example:
    python weather_checker.py "Pune" "Sunny"
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def check_weather(city, expected_condition):
    """
    Check weather for a given city and compare with expected condition.
    
    Args:
        city (str): The name of the city to check weather for
        expected_condition (str): The expected weather condition
        
    Returns:
        bool: True if actual weather contains expected condition, False otherwise
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Install and setup Chrome driver
        print(f"Setting up WebDriver...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Navigate to Google Weather for the specified city
        url = f"https://www.google.com/search?q=weather+{city.replace(' ', '+')}"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for the weather condition element to be present
        print("Extracting weather information...")
        wait = WebDriverWait(driver, 10)
        weather_element = wait.until(
            EC.presence_of_element_located((By.ID, "wob_dc"))
        )
        
        # Extract the actual weather condition
        actual_condition = weather_element.text.strip()
        print(f"Current weather in {city}: {actual_condition}")
        
        # Compare with expected condition (case-insensitive)
        is_match = expected_condition.lower() in actual_condition.lower()
        result_message = (
            f"✅ Weather matches your expectation!" 
            if is_match 
            else f"❌ Weather doesn't match your expectation."
        )
        print(result_message)
        print(f"Expected: {expected_condition}")
        print(f"Actual: {actual_condition}")
        
        # Capture a screenshot of the weather information
        screenshot_path = f"{city.replace(' ', '_')}_weather.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")
        
        return is_match
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()
            print("Browser closed.")

def main():
    """
    Main function to parse command line arguments and check weather.
    """
    # Check if correct number of arguments provided
    if len(sys.argv) != 3:
        print("Usage: python weather_checker.py <city_name> <expected_condition>")
        print("Example: python weather_checker.py \"Pune\" \"Sunny\"")
        sys.exit(1)
    
    # Extract command line arguments
    city = sys.argv[1]
    expected_condition = sys.argv[2]
    
    print(f"Weather Checker Agent Started")
    print(f"Checking if the weather in {city} is {expected_condition}...")
    print("-" * 50)
    
    # Check the weather
    result = check_weather(city, expected_condition)
    
    print("-" * 50)
    print("Weather Checker Agent Completed")
    
    # Return exit code based on whether expectation was met
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()