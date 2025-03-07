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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
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
        
        # Wait for page to load completely
        time.sleep(3)
        print("Waiting for page to load completely...")
        
        # Multiple possible selectors for weather condition
        possible_selectors = [
            (By.ID, "wob_dc"),  # Traditional ID
            (By.CSS_SELECTOR, ".wob_dc"),  # Class name
            (By.XPATH, "//div[contains(@class, 'wob_dc')]"),  # XPath with class
            (By.XPATH, "//div[@id='wob_dcp']/div"),  # Parent container's child
            (By.XPATH, "//div[contains(@aria-label, 'Weather')]//div[contains(@data-local-attribute, 'weather-condition')]"),  # Semantic approach
            (By.XPATH, "//div[contains(text(), '°')]/..//span"),  # Near temperature element
            (By.XPATH, "//div[@class='UQt4rd']")  # General weather container
        ]
        
        # Try each selector until one works
        actual_condition = None
        for selector_type, selector_value in possible_selectors:
            try:
                print(f"Trying to find weather element with {selector_type}: {selector_value}")
                wait = WebDriverWait(driver, 5)
                weather_element = wait.until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                actual_condition = weather_element.text.strip()
                if actual_condition:
                    print(f"Found weather condition using {selector_type}: {selector_value}")
                    break
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Selector {selector_value} failed: {str(e)}")
                continue
        
        # If no selector worked, try to get any text that might contain weather info
        if not actual_condition:
            print("Couldn't find weather with specific selectors, trying general approach...")
            try:
                # Take a screenshot for debugging
                debug_screenshot = f"{city.replace(' ', '_')}_debug.png"
                driver.save_screenshot(debug_screenshot)
                print(f"Debug screenshot saved as {debug_screenshot}")
                
                # Try to find any element with weather-related text
                page_text = driver.page_source.lower()
                common_conditions = [
                    "sunny", "cloudy", "rain", "partly", "clear", "storm", 
                    "snow", "fog", "mist", "drizzle", "overcast", "haze"
                ]
                
                # Look for common weather terms in the page
                for condition in common_conditions:
                    if condition in page_text:
                        # Try to get text from elements near this term
                        elements = driver.find_elements(By.XPATH, f"//div[contains(text(), '{condition}')]")
                        if elements:
                            actual_condition = elements[0].text.strip()
                            print(f"Found likely weather condition: {actual_condition}")
                            break
            except Exception as e:
                print(f"Alternative approach failed: {e}")
        
        # If still no condition found, look at page title which often contains weather info
        if not actual_condition:
            title = driver.title
            if "weather" in title.lower():
                parts = title.split('-')
                if len(parts) > 1:
                    actual_condition = parts[0].strip()
                    print(f"Extracted condition from page title: {actual_condition}")
        
        # Final check if we found anything
        if not actual_condition:
            print("Couldn't extract weather condition. Please check the website structure.")
            return False
            
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
        if 'driver' in locals():
            print("Taking debug screenshot...")
            driver.save_screenshot(f"{city.replace(' ', '_')}_error.png")
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