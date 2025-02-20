import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from db.index import  MongoDBHandler
from dotenv import load_dotenv

load_dotenv()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

def convert_to_float(s):
    try:
        # Remove commas
        s = s.replace(',', '')
        return float(s)
    except ValueError:
        raise ValueError(f"Cannot convert '{s}' to float.")


def get_emissions_stats():  
    stats = dict()  
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator?unit=MCF&amount=1#results')
    results_table = driver.find_element(By.ID, "results_table")
    result_containers = results_table.find_elements(By.XPATH, "//div[contains(@class, 'roundbox-container')]")
    for container in result_containers:
        round_boxes = container.find_elements(By.TAG_NAME, "div")
        for round_box in round_boxes:
            value = round_box.find_element(By.TAG_NAME,"input").get_attribute("value")
            description = round_box.find_element(By.TAG_NAME,"p").text
            print("stat", value, description)
            if "homes' energy use" in description:
                stats["home_enery_use_one_year"] = value
            if "gallons of diesel" in description:
                stats["diesel_gallons"] = value
            if "smartphones" in description:
                stats["smartphones_charged"] = value

    print(stats)
    driver.close()

    handler = MongoDBHandler(
        uri= os.environ.get("DB_URL"),
        db_name= os.environ.get("DB_NAME"),
        collection_name=os.environ.get("COLLECTION_NAME")
    )

    handler.connect()
    handler.save_emission(convert_to_float(stats["home_enery_use_one_year"]), convert_to_float(stats["diesel_gallons"]), convert_to_float(stats["smartphones_charged"]), 2, 8, 2025)
    
if __name__ == '__main__':
    get_emissions_stats()
