import asyncio
import json
from pyppeteer import page  




async def login_to_stealth_writer(page, email, password):
    try:
        # Find email & input 
        await asyncio.sleep(1)  
        await page.waitForSelector('input[name="email"]')
        print('Entering Email')
        await page.type('input[name="email"]', email)

        print('Entering Password')
        await page.type('input[name="password"]', password)

        # print('Solving Captcha...')
        
        # await page.solveRecaptchas()  

        # Login button click
        await asyncio.sleep(1)  
        await asyncio.gather(
            page.waitForNavigation(),
            page.click('button[type="submit"]')
        )
        print("Login Button Clicked")
        
        await asyncio.sleep(1)  
        # Save the cookies
        print('Saving Cookies')
        cookies = await page.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)
        print('Done Saving Cookies')

        print('Saving Cookies and Local Storage Data')
        local_storage_data = await page.evaluate('JSON.stringify(window.localStorage)')
        
        with open('localStorage.json', 'w') as f:
            f.write(local_storage_data)
        print('Done Saving Cookies and Local Storage Data')



    except Exception as error:
        print('Error occurred in login:', error)

# If you want to export the function for use in another module
# if __name__ == "__main__":
#     pass  # You can add testing or calling code here
