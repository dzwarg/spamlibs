import asyncio
import json
from playwright.async_api import Playwright, async_playwright, expect

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        # Intercept network requests
        async def handle_route(route):
            if route.request.url == "http://127.0.0.1:8000/webhook/incoming" and route.request.method == "POST":
                print("Intercepted POST request to /webhook/incoming")
                
                # Assertions
                assert route.request.method == "POST"
                assert "application/json" in route.request.headers['content-type']
                
                expected_payload = {
                    "subject": "Message from the form",
                    "from": {
                        "value": [
                            {
                                "address": "form@example.com",
                                "name": "Form User"
                            }
                        ]
                    },
                    "text": "This is a test message."
                }
                
                # Compare the request's post data with the expected payload
                assert json.loads(route.request.post_data) == expected_payload
                
                # Fulfill the request to let it continue to the server
                await route.fulfill(status=200, body=json.dumps({"status": "ok"}))
            else:
                await route.continue_()

        await page.route("**/*", handle_route)

        await page.goto("http://127.0.0.1:8000/")

        # Fill the form and submit
        await page.fill("textarea#message", "This is a test message.")
        await page.click("input[type=submit]")

        # Wait for the response (or a timeout)
        await page.wait_for_timeout(1000) # Wait for 1 second to ensure the request is caught

        # Assert that the success indicator is visible
        await expect(page.locator("#submissionStatus")).to_be_visible()

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
