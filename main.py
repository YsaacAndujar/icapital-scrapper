import asyncio
from playwright.async_api import async_playwright, Playwright
import json

async def run(playwright: Playwright):
    browser = await playwright.chromium.launch(headless=False)

    context = await browser.new_context(
        locale='en-CA', 
        extra_http_headers={
            'Accept-Language': 'en-CA,en;q=0.9'
        }
    )

    page = await context.new_page()
    await page.goto("https://icapital.com/careers/")
    print("Searching for jobs...")
    office_option_value = await page.locator("#filter_office >> option", has_text="CA ON - Toronto").get_attribute("value")
    emp_type_option_value = await page.locator("#filter_emp_type >> option", has_text="Full-time").get_attribute("value")
    ids = set(emp_type_option_value.split(',')) & set(office_option_value.split(','))
    job_result = []
    for id in ids:
        el = page.locator(f'[data-id="{id}"]')
        title = await el.locator('.job_title').inner_text()
        position_unformatted = await el.locator('.display_location').inner_text()
        position = position_unformatted.removeprefix('Location: ')
        description_unformatted = await el.locator('.job_description').inner_text()
        description = description_unformatted.strip()
        
        job_result.append({
            "title": title,
            "position": position,
            "description": description
        })
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(job_result, f, indent=2, ensure_ascii=False)
    print('Search completed. jobs.json file created with job listings.')
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
