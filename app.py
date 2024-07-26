import os
import logging
from flask import Flask, render_template, request, redirect, url_for
import aiohttp
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.common.exceptions import WebDriverException

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configure logging
logging.basicConfig(level=logging.INFO, filename='website_health.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

websites = app.config['WEBSITES']
website_status = {}

async def check_dns(domain):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"http://{domain}", timeout=20) as response:
                return response.status == 200
        except Exception as e:
            logging.error(f"DNS check failed for {domain}: {e}")
            return False

async def take_screenshot(url, domain):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    screenshot_path = f'static/screenshots/{domain}.png'

    try:
        driver.get(f"http://{domain}")
        driver.set_window_size(1920, 1080)
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    except Exception as e:
        logging.error(f"Error taking screenshot for {domain}: {e}")
        return None
    finally:
        driver.quit()

async def check_website(url, domain):
    result = {
        'dns': False,
        'ssl': False,
        'online': False,
        'error': None,
        'screenshot': None,
        'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        result['dns'] = await check_dns(domain)
        if result['dns']:
            result['screenshot'] = await take_screenshot(url, domain)
            result['online'] = True if result['screenshot'] else False
    except WebDriverException as e:
        result['error'] = str(e)
        logging.error(f"Error checking {domain}: {e}")
    except Exception as e:
        result['error'] = str(e)
        logging.error(f"Unexpected error checking {domain}: {e}")

    return result

async def check_websites_async():
    tasks = [check_website(url, url) for url in websites]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for website, result in zip(websites, results):
        if isinstance(result, Exception):
            website_status[website] = {'error': str(result)}
        else:
            website_status[website] = result

@app.route('/')
async def index():
    await check_websites_async()
    return render_template('index.html', results=website_status)

@app.route('/add', methods=['POST'])
def add_website():
    url = request.form['url']
    logging.info(f"Received URL to add: {url}")
    if url and url not in websites:
        websites.append(url)
        asyncio.run(check_websites_async())
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)