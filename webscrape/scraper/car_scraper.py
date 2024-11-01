import time
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Get the absolute path to the current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to cookies.pkl for consent cookies
COOKIES_PATH = os.path.join(BASE_DIR, "cookies.pkl")

def load_cookies(driver):
    try:    
        # Load cookies from the pickle file
        with open(COOKIES_PATH, "rb") as file:
            cookies = pickle.load(file)
        
        # Add each cookie to the driver
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        # Refresh to apply cookies
        driver.refresh()
        print("Cookies loaded successfully")
        return driver
    except Exception as e:
        print(f"Error loading cookies: {str(e)}")

def get_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-software-rasterizer")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def select_option_if_exists(driver, element_identifier, value, by=By.ID, max_attempts=4):
    attempt = 0
    delay = 0.3  # Start with a short delay
    
    while attempt < max_attempts:
        try:
            # Try locating the element within a short wait time
            select_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, element_identifier)))
            select = Select(select_element)
            
            # Check if the value exists in the dropdown options
            options = [option.text for option in select.options]
            if value in options:
                select.select_by_visible_text(value)
                return True  # Return True if selection was successful
        
        except Exception:
            attempt += 1
            delay += 0.3

    print(f"Error selecting '{value}' for '{element_identifier}': Element not found within max attempts")
    return False

def scrape_cars(job_data : dict, URL : str) -> dict:
    driver = get_selenium_driver()
    missing_filters = []  # List to track any unavailable filters

    try:
        if job_data.get("pageUrl") is None:
            driver.get(URL)
            load_cookies(driver)
            # Click the Advanced Search button
            search_extra_button = driver.find_element(By.ID, "search-extra-button")
            search_extra_button.click()

            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Scroll back up to the top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
        
            # Check and select each filter if available, using appropriate By method where necessary
            if (job_data.get("brand") is not None) and (not select_option_if_exists(driver, "for-make", job_data.get("brand"))):
                missing_filters.append("Brand: " + job_data.get("brand", "Unknown"))

            if (job_data.get("model") is not None) and (not select_option_if_exists(driver, "for-model", job_data.get("model"))):
                missing_filters.append("Model: " + job_data.get("model", "Unknown"))

            if (job_data.get("yearStart") is not None) and (not select_option_if_exists(driver, "for-yearFrom", str(job_data.get("yearStart")))):
                missing_filters.append("Year Start: " + str(job_data.get("yearStart", "Unknown")))

            if (job_data.get("yearEnd") is not None) and (not select_option_if_exists(driver, "widget[yearTo]", str(job_data.get("yearEnd")), by=By.NAME)):
                missing_filters.append("Year End: " + str(job_data.get("yearEnd", "Unknown")))

            if (job_data.get("fuelType") is not None) and (not select_option_if_exists(driver, "for-fuel", job_data.get("fuelType"))):
                missing_filters.append("Fuel Type: " + job_data.get("fuelType", "Unknown"))

            if (job_data.get("transmission") is not None) and (not select_option_if_exists(driver, "for-gear", job_data.get("transmission"))):
                missing_filters.append("Transmission: " + job_data.get("transmission", "Unknown"))
            
            # For Disassembled Cars there is no price range
            if job_data.get("notificationType") != "disassembled_car":
                if (job_data.get("priceFrom") is not None) and (not select_option_if_exists(driver, "for-priceFrom", str(job_data.get("priceFrom")))):
                    missing_filters.append("Price From: " + job_data.get("priceFrom", "Unknown"))

                if (job_data.get("priceTo") is not None) and (not select_option_if_exists(driver, "widget[priceTo]", str(job_data.get("priceTo")), by=By.NAME)):
                    missing_filters.append("Price To: " + job_data.get("priceTo", "Unknown"))

            if (job_data.get("color") is not None) and (not select_option_if_exists(driver, "for-color", job_data.get("color"))):
                missing_filters.append("Color: " + job_data.get("color", "Unknown"))

            if (job_data.get("bodyType") is not None) and (not select_option_if_exists(driver, "for-bodyType", job_data.get("bodyType"))):
                missing_filters.append("Body Type: " + job_data.get("bodyType", "Unknown"))

            if (job_data.get("origin") is not None) and (not select_option_if_exists(driver, "for-origin", job_data.get("origin"))):
                missing_filters.append("Origin: " + job_data.get("origin", "Unknown"))

            # If any filters are missing, return a message and stop further processing
            if missing_filters:
                return {
                    "status": "warning",
                    "userId": job_data.get("userId"),
                    "message": "The following filters are not available in the catalog:\n" + ", ".join(missing_filters)
                }

            # Click the search button
            search_button = driver.find_element(By.ID, "search-button")
            driver.execute_script("arguments[0].click();", search_button)

            # Check for "not available" message
            try:
                no_results_element = driver.find_element(By.CLASS_NAME, "search-not-found")
                if no_results_element.is_displayed():
                    return {"status": "not_available", "userId": job_data.get("userId"), "message": "No listings found for the specified filters."}
            except:
                pass

            # Extract car listings if available (first page only)
            listings = []
            newVehicleCount = 0
            car_elements = driver.find_elements(By.CSS_SELECTOR, ".grid .flexitem.car")
            for car in car_elements:
                try:
                    title = car.find_element(By.CSS_SELECTOR, "h2 a").text
                    price = car.find_element(By.CLASS_NAME, "price").text if car.find_elements(By.CLASS_NAME, "price") else None
                    details = car.find_element(By.CLASS_NAME, "details").text
                    car_url = car.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    image_url = car.find_element(By.CSS_SELECTOR, ".car-image img").get_attribute("src")
                    new_label = car.find_element(By.CSS_SELECTOR, ".label-new").text if car.find_elements(By.CSS_SELECTOR, ".label-new") else None
                    if new_label:
                        newVehicleCount += 1

                        listings.append({
                            "title": title,
                            "price": price,
                            "details": details,
                            "url": car_url,
                            "image_url": image_url,
                            "new_label": new_label
                        })
                except Exception as e:
                    print(f"Error parsing car listing: {e}")

            if newVehicleCount > job_data.get("currentVehicleCount"):
                return {
                    "status": "available",
                    "userId": job_data.get("userId"),
                    "listings": listings,
                    "newVehicleCount": newVehicleCount,
                    "pageUrl": driver.current_url
                }
            else:
                return {"status": "not_available", "userId": job_data.get("userId"), "message": "No new listings found for the specified filters."}
        else:
            # Extract car listings if available (first page only) from the existing page_url to prevent rescraping
            driver.get(job_data.get("pageUrl"))
            load_cookies(driver)
            listings = []
            newVehicleCount = 0
            car_elements = driver.find_elements(By.CSS_SELECTOR, ".grid .flexitem.car")
            for car in car_elements:
                try:
                    title = car.find_element(By.CSS_SELECTOR, "h2 a").text
                    price = car.find_element(By.CLASS_NAME, "price").text if car.find_elements(By.CLASS_NAME, "price") else None
                    details = car.find_element(By.CLASS_NAME, "details").text
                    car_url = car.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    image_url = car.find_element(By.CSS_SELECTOR, ".car-image img").get_attribute("src")
                    new_label = car.find_element(By.CSS_SELECTOR, ".label-new").text if car.find_elements(By.CSS_SELECTOR, ".label-new") else None
                    if new_label:
                        newVehicleCount += 1

                        listings.append({
                            "title": title,
                            "price": price,
                            "details": details,
                            "url": car_url,
                            "image_url": image_url,
                            "new_label": new_label
                        })
                except Exception as e:
                    print(f"Error parsing car listing: {e}")

            if newVehicleCount > job_data.get("currentVehicleCount"):
                return {
                    "status": "available",
                    "userId": job_data.get("userId"),
                    "listings": listings,
                    "newVehicleCount": newVehicleCount,
                    "pageUrl": driver.current_url
                }
            else:
                return {"status": "not_available", "userId": job_data.get("userId"), "message": "No new listings found for the specified filters."}

    finally:
        driver.quit()

def scrape_starter(job_data : dict) -> dict:
    URLS = {
            "damaged_car": "https://www.schadeautos.nl/en/damaged-car",
            "disassembled_car": "https://www.schadeautos.nl/en/salvage-car",
            "used_car": "https://www.schadeautos.nl/en/occasion-passenger-cars",
            }
    
    if job_data['notificationType'] == 'damaged_car':
        results = scrape_cars(job_data, URLS["damaged_car"])
        return results
   
    elif job_data['notificationType'] == 'disassembled_car':
        results = scrape_cars(job_data, URLS["disassembled_car"])
        return results

    elif job_data['notificationType'] == 'used_car':
        results = scrape_cars(job_data, URLS["used_car"])
        return results

if __name__ == "__main__":
    
    job_data = {
        "notificationType": "damaged_car",
        "brand": "Mercedes",
        "model": None,
        "yearStart": "1958",
        "yearEnd": "2023",
        "fuelType": None,
        "transmission": None,
        "priceFrom": None,
        "priceTo": None,
        "color": "white",
        "bodyType":None,
        "origin": None,
        "pageUrl": "https://www.schadeautos.nl/en/search/damaged/passenger-cars+mercedes/1/1/53/0/0/0/1/0?color=29&p=-2023",
        "currentVehicleCount": 6
    }

    results = scrape_starter(job_data)
    print(results)