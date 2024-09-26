import asyncio
from pyppeteer import launch
from stealthwriter.login import login_to_stealth_writer
from stealthwriter.humanizerPg import goto_humanizerPg
from stealthwriter.textHumanize import text_humanizer
from database.connections import *
import re

def split_into_sentences(paragraph):
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    return sentences

async def stealth_ai_login(email, password):
    try:
        browser = await launch(
        executablePath='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        headless= True
            # 'args': ['--no-sandbox']
        )

        page = await browser.newPage()
        
        await page.goto('https://app.stealthwriter.ai/dashboard', {'waitUntil': 'domcontentloaded'})
        await page.waitForSelector('body')
        await page.setViewport({'width': 1920, 'height': 1080}) 
    
        current_url = page.url

        print("========Login phase=========")
        if 'login' in current_url:
            await login_to_stealth_writer(page, email, password)
            print("Done Login.....!!")   
            
            # Close the popup window on dashboard
            await asyncio.sleep(2)
            try:
                close_btn = await page.waitForXPath('//button[text()="Close"]', {'timeout': 5000})
                if close_btn:
                    await close_btn.click()
                    print("Close button clicked.")
            except Exception as e:
                print("No close button found after login.", e)
            
        print("========Go to Humanizer Page=========")
        await asyncio.sleep(2)
        await goto_humanizerPg(page)

        print("========Text Humanizing=========")        
        db=connect_to_mongo()
        j=0
        while True:
            scraping_doc = fetch_text_form_scrapingDb(db)  
            print(f"<=============For Data {j+1} stealth writing processing==========>")
            j += 1
            data_id = scraping_doc['_id']
            paragraph = scraping_doc['text']
            humanize_text = None

            if not scraping_doc:
                print("No more Data found From Scraping Database.")
                break  

            sentences = split_into_sentences(paragraph)
            documents = []
            print("No of Total Sentences:", len(sentences))
            total_sentences = len(sentences)
            for i, sentence in enumerate(sentences):
                i += 1
                document = {
                    'input_Text': sentence,
                    'humanized_text': None,
                    'scraping_id' : data_id,
                    'sentence_no' : i,
                }
                print(f"<=========== For sentence {i}/{total_sentences} of data {j} ==============>")
                characters_count = len(sentence)
                print("Number of Characters:", characters_count)

                if characters_count > 50:
                    try:
                        humanize_texts = await text_humanizer(page, sentence)
                        no_of_demo=len(humanize_texts)
                        print("Input Text:", sentence,"\nNo of Demo:",no_of_demo ,"\nOutput Text:", humanize_texts)

                        if humanize_texts:
                            document['humanized_text'] = humanize_texts

                    except Exception as e:
                        print("Error occurred during humanization:", e)

                else:
                    print("Character count is less than 50, skipping humanization.")
                    continue

                documents.append(document)

            # Store humanized texts
            store_humanized_text(db, documents, data_id)
            print("Waiting for the next paragraph...")
            await asyncio.sleep(1)  

        print("========No More Data to Process=========")
        await browser.close()
        return True
    
    except Exception as error:
        print('Error Occurred on stealthAiLogin Pyppeteer:', error)
        return False


if __name__ == "__main__":
    email = "abdullahalmahmud.cse007@gmail.com"
    password = "1234567890"
    asyncio.get_event_loop().run_until_complete(stealth_ai_login(email, password))