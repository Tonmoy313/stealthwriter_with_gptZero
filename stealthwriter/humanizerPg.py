import asyncio
async def goto_humanizerPg(page):
    try:
        # click to the Humanizer panel button
        await asyncio.sleep(1)
        print("Going the Humanizer Pannel")
        await page.waitForSelector('a[href="/humanizer"]')
        await page.click('a[href="/humanizer"]')
        
        # Close the popup window on humanizer panel
        await asyncio.sleep(2) 
        # close_btn_element=  'button.inline-flex.items-center' 
        close_btn_element=  'button[type="button"].absolute.right-4.top-4.rounded-sm.opacity-70'
        await page.waitForSelector(close_btn_element)
        await page.click(close_btn_element)
        print("Pop-up closed")

    except Exception as e:
        print(f"Error: {e}")