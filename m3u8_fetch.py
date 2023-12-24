import time
import json
from seleniumwire import webdriver
from flask import Flask, request

app = Flask(__name__)

def fetch_playable_url(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    start_time = time.time()
    timeout = 20 # Set a timeout of 20 seconds
    playable_url = ""
    headers = ""

    while time.time() - start_time < timeout:
        for req in driver.requests:
            if '.m3u8' in req.url:
                playable_url = req.url
                headers = str(req.headers)
                driver.quit()
                return playable_url, headers

        time.sleep(1)

    driver.quit()  # Quit the driver if the timeout is reached without finding the URL
    return playable_url, headers


@app.route('/api/get_url', methods=['GET'])
def get_url():
    url = request.args.get('url')
    playable, header = fetch_playable_url(url)
    res = {"url": playable, "headers": header}

    return res


if __name__ == '__main__':
    app.run()
