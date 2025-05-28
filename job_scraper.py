## This script scrapes job listings from Indeed using Selenium.
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_indeed_jobs(query, location="Ottawa", use_mock=False):
    
    # Testing with mock data if use_mock is True
    if use_mock:
        return [
            "Software Developer: Develop web applications using Python and JavaScript frameworks.",
            "Full Stack Developer: Build and maintain web applications using React and Node.js.",
            "Python Developer: Develop backend services using Python, Django and Flask.",
            "Software Engineer: Design and implement scalable software solutions.",
            "Web Developer: Create responsive web applications with modern frameworks."
        ]

    # Selenium implementation to scrape Indeed jobs
    jobs = []
    
    # Set up Chrome options with improved anti-detection measures
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    
    # Add a realistic user agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Try using the regular Indeed domain
        url = f"https://www.ca.indeed.com/jobs?q={query}&l={location}"
        driver.get(url)
        
        # Add a realistic delay
        time.sleep(3)
        
        # Wait for job cards to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-ResultsList"))
        )
        
        # Extract job information
        job_cards = driver.find_elements(By.CSS_SELECTOR, ".job_seen_beacon, .tapItem")
        
        for job_card in job_cards:
            try:
                title_element = job_card.find_element(By.CSS_SELECTOR, "h2.jobTitle span, h2.jobTitle a")
                
                # Try different selectors for the description
                try:
                    desc_element = job_card.find_element(By.CSS_SELECTOR, "div.job-snippet")
                except:
                    try:
                        desc_element = job_card.find_element(By.CSS_SELECTOR, ".job-snippet-container")
                    except:
                        desc_element = job_card.find_element(By.CSS_SELECTOR, "[id^='jobDescriptionText']")
                
                title = title_element.text
                desc = desc_element.text.strip()
                
                jobs.append(f"{title}: {desc}")
            except Exception as e:
                print(f"Error extracting job details: {e}")
                continue
                
    except Exception as e:
        print(f"Error during scraping: {e}")
        print("Falling back to mock data due to scraping issues")
        return scrape_indeed_jobs(query, location, use_mock=True)
    
    finally:
        # Always close the driver
        driver.quit()
        
    return jobs
