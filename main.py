import asyncio
from playwright.async_api import async_playwright, Playwright
import json

async def run(playwright: Playwright):
    browser = await playwright.chromium.launch()

    context = await browser.new_context(
        locale='en-CA', 
        extra_http_headers={
            'Accept-Language': 'en-CA,en;q=0.9'
        }
    )

    page = await context.new_page()
    await page.goto("https://icapital.com/careers/")
    print("Searching for jobs...")
    await page.locator('#filter_office').select_option(label='CA ON - Toronto')
    await page.locator('#filter_emp_type').select_option(label='Full-time')
    all_jobs = page.locator('.job')
    count = await all_jobs.count()
    job_result = []
    for i in range(count):
        el = all_jobs.nth(i)
        display = await el.evaluate("e => getComputedStyle(e).display")
        if display != 'grid':
            continue
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
