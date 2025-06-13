from playwright.async_api import async_playwright

async def fetch_episode_links(main_url):
    episode_data = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(main_url, timeout=60000)

        # Get all episode elements (you may need to customize this selector)
        episode_links = await page.eval_on_selector_all(
            'a[href*="WatchMultiQuality"]',
            'elements => elements.map(e => e.href)'
        )

        for idx, ep_link in enumerate(episode_links, start=1):
            try:
                await page.goto(ep_link, timeout=60000)
                await page.wait_for_selector('a:has-text("Download")')
                await page.click('a:has-text("Download")')

                await page.wait_for_url("**/download/**", timeout=30000)

                # Now we are on the page with 360p/720p/1080p
                links = await page.eval_on_selector_all(
                    'a[href*="multiquality.click/download"]',
                    'elements => elements.map(e => ({text: e.innerText, href: e.href}))'
                )

                episode_data[f"{idx:02}"] = {
                    l["text"]: l["href"] for l in links
                }

            except Exception as e:
                episode_data[f"{idx:02}"] = {"Error": str(e)}
                continue

        await browser.close()

    return episode_data
