import asyncio
from playwright.async_api import Playwright, async_playwright, expect

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:8080/")
        await expect(page.locator("h1")).to_have_text("Spamlibs")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
