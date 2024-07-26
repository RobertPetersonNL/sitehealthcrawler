import sys
import asyncio
from pyppeteer import launch

async def capture_screenshot(url, filename):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await page.screenshot({'path': filename, 'fullPage': True})
    await browser.close()

if __name__ == "__main__":
    url = sys.argv[1]
    filename = sys.argv[2]
    asyncio.get_event_loop().run_until_complete(capture_screenshot(url, filename))