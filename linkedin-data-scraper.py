import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_linkedin():
    # Set up the Chrome driver
    service = Service('path_to_chromedriver')
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    try:
        # Open LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("your_email@example.com")
        driver.find_element(By.ID, "password").send_keys("your_password")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Perform Google search for LinkedIn profiles
        search_query = "site:linkedin.com 'IIT graduate'"
        driver.get(f"https://www.google.com/search?q={search_query}")
        time.sleep(2)

        profiles = []
        search_results = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/a")
        for result in search_results[:10]:
            profile_link = result.get_attribute("href")
            driver.get(profile_link)
            time.sleep(2)

            # Scrape job title, company, and industry
            try:
                job_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class,'t-18')]"))).text
                company = driver.find_element(By.XPATH, "//a[contains(@href, '/company/')]").text
                industry = driver.find_element(By.XPATH, "//li[contains(text(),'Industry')]").text.split(":")[-1].strip()
                profiles.append({"Job Title": job_title, "Company": company, "Industry": industry})
            except NoSuchElementException:
                continue

        # Save data to CSV
        with open("iit_graduates.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Job Title", "Company", "Industry"])
            writer.writeheader()
            writer.writerows(profiles)

    except TimeoutException:
        print("A timeout occurred.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Run the scraper
scrape_linkedin()
