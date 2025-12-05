🎬 Live Cinema Occupancy Tracker
A robust Python automation tool designed to extract real-time seating and occupancy data from BookMyShow. Unlike standard scrapers that only fetch surface-level data, this tool navigates into individual show seat layouts to calculate precise occupancy rates, gross revenue potential, and ticket sales trends.
🚀 Key Features
Smart Scheduling Engine: Instead of scraping sequentially, the script sorts shows by their cut-off time and intelligently halts execution (sleeps) until exactly 5 minutes before booking closes. This ensures data is captured at the peak of occupancy.
Deep Data Extraction: Navigates through the booking flow to the seat layout page, parsing the DOM to count specific HTML elements:
_available (Open seats)
_blocked (Sold seats)
Anti-Bot Evasion:
Utilizes undetected-chromedriver to bypass Cloudflare/WAF protections.
User-Agent Rotation: Randomizes mobile User-Agent strings for every session to mimic genuine traffic.
Human-Like Behavior: Implements random delays (random.uniform) and mouse movement logic to avoid bot detection.
Resilience: built-in exception handling for popups (btnPopupOK) and Sold Out scenarios.
🛠️ Tech Stack
Language: Python 3.x
Core Library: Selenium WebDriver
Driver: undetected-chromedriver (Chrome)
Logic: datetime for temporal scheduling
⚙️ How It Works
Initialization: Launches a Chrome instance with a randomized User-Agent and suppressed automation flags.
Discovery: Scans the venue page and collects all showtime-pill elements.
Sorting: Parses the data-cut-off-date-time attribute and sorts the execution queue chronologically.
Execution Loop:
Calculates the time delta between now and show_end_time - 5 mins.
Suspends the thread until the target window is reached.
Enters the show, bypasses "Select Seats" prompts, and scrapes the seat matrix.
Calculates occupancy percentage: (Blocked / Total) * 100.
Returns to the listing page and repeats for the next show.
📦 Installation
pip install selenium undetected-chromedriver


⚠️ Disclaimer
This project is for educational purposes only. Automated scraping of websites may violate their Terms of Service. Ensure you have permission before scraping high-volume data.
