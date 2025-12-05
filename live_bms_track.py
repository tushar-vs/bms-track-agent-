from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
import random
import undetected_chromedriver as uc

options = Options()
user_agents = [
    "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7",
]

# Pick a random User-Agent
options.add_argument(f"user-agent={random.choice(user_agents)}")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-notifications')

driver = uc.Chrome(options=options)

# Open the BookMyShow URL
driver.get("bookmyshow_link")
time.sleep(random.uniform(5,10))

def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

try:
    # Locate all show elements and collect their data
    total_show_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'showtime-pill')]")
    print(f"Total Number of Shows: {len(total_show_elements)}")
    time.sleep(random.uniform(2, 4))

    show_data = []
    select_seats_clicked = False
    for show in total_show_elements:
        # Extract show details
        show_end = show.get_attribute("data-cut-off-date-time")  
        if not show_end:  # Skip shows with no `data-cut-off-date-time
            print("Skipping a show without `data-cut-off-date-time`.")
            continue


        show_code = show.get_attribute("data-showtime-code")
        show_time=show.get_attribute("data-showtime-filter-index")
        show_venue=show.get_attribute("data-venue-code")
        show_element = show
        
        # Convert `data-cutoff-date-time` to a datetime object
        show_end_datetime = datetime.strptime(show_end, "%Y%m%d%H%M")
        
        # Add to show data list
        show_data.append({
            "show_code": show_code,
            "show_end_datetime": show_end_datetime,
            "show_element": show_element,
            "show_time":show_time,
            "show_venue":show_venue
        })

    # Sort the shows by their end time
    show_data.sort(key=lambda x: x["show_end_datetime"])

    print("Shows sorted by end time.")

    # Continuously monitor the time and perform actions
    for show in show_data:
        show_code = show["show_code"]
        show_end_datetime = show["show_end_datetime"]
        show_element = show["show_element"]
        show_time=show["show_time"]
        show_venue=show["show_venue"]

        # Calculate the time to wait until 5 minutes before the end time
        current_datetime = datetime.now()
        action_time = show_end_datetime - timedelta(minutes=5)
        time_to_wait = (action_time - current_datetime).total_seconds()

        if time_to_wait > -120:  # Allow action even within 2 minutes past cutoff
            print(f"Waiting {max(0, time_to_wait):.2f} seconds to perform action for Show Code: {show_code}")
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            

            # Check if the show is sold out before clicking
            parent_container = show_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'showtime-pill-container')]")
            if "_sold" in parent_container.get_attribute("class"):
                print(f"Show Code {show_code} is now sold out. Skipping...")
                continue

            try:
                show_element.click()
                time.sleep(4)  # Allow time for any errors to propagate

                

                # Handle popup if displayed
                try:
                    popup_ok_button = WebDriverWait(driver, 6).until(
                        EC.element_to_be_clickable((By.ID, "btnPopupOK"))
                    )
                    popup_ok_button.click()
                    print("Popup OK button clicked.")
                except Exception:
                    print("No popup found, proceeding.")

                if not select_seats_clicked:
                    try:
                        select_seats_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@id='proceed-Qty' and contains(@class, 'bar-btn') and contains(text(), 'Select Seats')]"))
                        )
                        select_seats_button.click()
                        select_seats_clicked = True
                        random_delay(2, 4)
                    except Exception as e:
                        print("Error clicking Select Seats button:", e)

                # Count available and booked seats
                available_seats = driver.find_elements(By.XPATH, "//a[contains(@class, '_available') and starts-with(@onclick, 'fnSelectSeat')]")
                booked_seats = driver.find_elements(By.XPATH, "//a[contains(@class, '_blocked')]")
                seats_sold=len(booked_seats)
                total_seats = len(available_seats) + len(booked_seats)
                occupancy = (len(booked_seats) / total_seats) * 100 if total_seats > 0 else 0

                print(f"total seats :{total_seats}  tickets sold:{seats_sold}  occupancy:{occupancy}  showtime:{show_end_datetime}  showyavaga:{show_yavaga} show_venue:{show_venue}  ")
                
                # Navigate back to the previous page
                back_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@id='disback']"))
                )
                back_button.click()
                random_delay()

            except Exception as e:
                print(f"Error processing Show Code {show_code}: {e}")
                continue  # Move to the next show if there's an error

        else:
            print(f"Skipping action for Show Code: {show_code} as it's past the 2-minute grace period.")

except Exception as e:
    print(f"Error processing shows: {e}")

# Close the driver
driver.quit()
