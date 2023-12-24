from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Set the URL of the live stream page
stream_page_url = "http://cdn.buffsports.stream/webplayer.php?t=ifr&c=2150044&lang=en&eid=137968178&lid=2150044&ci=258&si=4&ask=1685475000"

# Configure the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode, without opening a browser window

# Use the Service object from webdriver_manager to handle the WebDriver executable
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=options)

# Load the stream page
driver.get(stream_page_url)

# Extract the .m3u8 link from the page source
page_source = driver.page_source
m3u8_link = None
if page_source:
    start_index = page_source.find(".m3u8")
    if start_index != -1:
        end_index = page_source.find("\n", start_index)
        m3u8_link = page_source[start_index:end_index]

if m3u8_link:
    print("Found .m3u8 link:", m3u8_link)
else:
    print("No .m3u8 link found on the stream page.")

# Quit the WebDriver
driver.quit()
