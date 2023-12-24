from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
import json
import time

app = Flask(__name__)


@app.route('/extract_m3u8_links', methods=['POST'])
def extract_m3u8_links():
    # Get the JSON data from the request
    data = request.json

    # Extract the URL from the JSON data
    url = data['url']

    # Enable Network Logging
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    driver = webdriver.Chrome(desired_capabilities=caps)

    driver.get(url)

    # Wait for the page to fully load
    WebDriverWait(driver, 30)

    # Additional delay to allow JS scripts to load and execute
    time.sleep(10)

    # Extract network logs
    logs = driver.get_log('performance')

    m3u8_links = set()

    # Parse the logs
    for entry in logs:
        msg = json.loads(entry['message'])
        params = msg['message']['params']
        if 'request' in params and '.m3u8' in params['request'].get('url', ''):
            url = params['request']['url']
            m3u8_links.add(url)

    driver.quit()

    # Convert the set of links to a list
    m3u8_links = list(m3u8_links)

    # Return the links as a JSON response
    return jsonify({'m3u8_links': m3u8_links})

if __name__ == '__main__':
    app.run()