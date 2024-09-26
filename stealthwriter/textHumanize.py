import asyncio

async def text_humanizer(page, text):
    try:
        # click the textBox & input The text 
        await asyncio.sleep(1)
        text_area_selector='textarea[style="min-height: 40vh;"]'
        textarea_exists = await page.waitForSelector(text_area_selector, timeout=10000)
        if textarea_exists:
            # print("Text field found")
            await page.click(text_area_selector)
            await page.type(text_area_selector, text)
            await page.evaluate('(element) => element.dispatchEvent(new Event("input", { bubbles: true }))',textarea_exists)
            # await page.evaluate('(element, text) => { element.value = text; element.dispatchEvent(new Event("input", { bubbles: true })); }', textarea_exists, text)
            print("Text entered successfully")
            
            # for text input number count in humanize panel
            await asyncio.sleep(5)
            div_element = await page.waitForSelector('div.text-sm.text-gray-500', timeout=10000)
            text_content = await page.evaluate('(element) => element.textContent', div_element)
            charcaters_count = int(text_content.split('|')[0].strip().split()[0])             
            print(f"Chracters Counts on text Field: {charcaters_count}")
            
            if charcaters_count>50:
                # Humanize click
                await asyncio.sleep(1)
                humanize_button = await page.waitForXPath('//button[text()="Humanize"]', timeout=8000)
                if humanize_button:
                    print("Humanizing...")
                    await humanize_button.click()
                    
                    await asyncio.sleep(5) 
                    text= []
                    i=1
                    while True:
                        # Geting the output Text from span button 
                        await asyncio.sleep(1) 
                        span_element = await page.waitForSelector('span[type="button"]', timeout=10000)
                        if span_element:
                            print(f"Sample Output Text {i}")
                            i=i+1
                            text_content = await page.evaluate('(element) => element.textContent', span_element)
                            text.append(text_content)
                            
                        else:
                            print("Output Text not found.")
                            return None   
                        
                        # clicking to the next button 
                        await asyncio.sleep(1)
                        next_button_elements = await page.xpath('//button[normalize-space()="Next"]')
                        if next_button_elements:
                            print("The button is found...!!")
                            next_button = next_button_elements[0]       
                            is_disabled = await page.evaluate('(element) => element.hasAttribute("disabled")', next_button)
                            
                            if is_disabled:
                                print(f"The 'Next' button is disabled? =>{is_disabled}")
                                break
                            
                            # Click the next button
                            await next_button.click()  
                            print(f"The 'Next' button is disabled? =>{is_disabled}. \nClicked the 'Next' button. ")
                            
                            await asyncio.sleep(1)
                        else:
                            print("The 'Next' button is not found.")
                            break  
                    
                    # Find and click the trash button to Clear the input Text
                    await asyncio.sleep(1)
                    trash_button = await page.waitForSelector('button.inline-flex svg.lucide-trash2')
                    if trash_button:
                        await trash_button.click()
                        print("Found the Trash button. & clicked it")
                        
                    return text 
                else:
                    print("Couldn't Humanize/Can't Click the Humanize Button")   
            else:
                print("Characters aren't greater than > 50")
                return "Too short to Humanize"   
        else:
            print("Text field not found.")
            return None

    except Exception as e:
        print(f"Error occurred in text_humanizer: {e}")
        return None












 # Find the next Button way 1
                    # button_elements = await page.querySelectorAll('button')
                    # for button in button_elements:
                    #     button_text = await page.evaluate('(element) => element.textContent', button)
                    #     if button_text.strip() == "Next":  
                    #         is_disabled = await page.evaluate('(element) => element.hasAttribute("disabled")', button)
                    #         print(f'Is the "Next" button disabled? {is_disabled}') 
                    #         break
                    # else:
                    #     print("The 'Next' button is not found.") 
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
# div_element = await page.waitForSelector('div.text-sm.text-gray-500', timeout=60000)
    
#             text_content = await page.evaluate('(element) => element.textContent', div_element)
            
#             # Extract the number of words from the text content
#             # Assuming the text format is "0 characters | 0 words"
#             await asyncio.sleep(1)
#             charcaters_count = int(text_content.split('|')[0].strip().split()[0])             
#             print(f"Number of Characters: {charcaters_count}")
            
#             if charcaters_count>50:
#                 # click the 'Humanize' button
#                 humanize_button = await page.waitForXPath('//button[text()="Humanize"]', timeout=8000)
#                 if humanize_button:
#                     print("Humanizing...")
#                     await humanize_button.click()
                    
#                     await asyncio.sleep(5)
                    
#                     # Ouput from the span element
#                     print("Finding the output text...")

#                     # Getting The Draft Numbers
#                     draft_count_element = await page.waitForSelector('span.draft-count')
#                     if draft_count_element:
#                         draft_count_text = await page.evaluate('(element) => element.textContent', draft_count_element)
#                         print(f"Draft count: {draft_count_text}")
                        
#                         try:
#                             draft_count = int(draft_count_text.strip()[-1])
#                         except ValueError:
#                             print(f"Unable to convert draft count text to an integer: {draft_count_text}")
#                             draft_count = 0

#                         text = []
#                         for demo in range(draft_count):
#                             span_element = await page.waitForSelector('span[type="button"]')
#                             if span_element:
#                                 print(f"Found the span element on demo {demo + 1}")
#                                 text_content = await page.evaluate('(element) => element.textContent', span_element)
#                                 # print(f"Text content for demo {demo + 1}: {text_content}")
#                                 text.append(text_content)
#                             else:
#                                 print("Span element not found.")
#                                 return None
                            
#                             if demo < draft_count - 1:
#                                 print(f"Draft {demo + 1} out of {draft_count}, clicking the 'Next' button...")

#                                 next_button_selector = 'button.inline-flex:has-text("Next")'
#                                 next_button = await page.waitForSelector(next_button_selector)
#                                 if next_button:
#                                     print("Found the 'Next' button.")
#                                     await next_button.click()
#                                     await asyncio.sleep(1)  
#                                 else:
#                                     print("'Next' button not found.")
#                             else:
#                                 print(f"Reached the last demo ({demo + 1}), no need to click 'Next'.")
                    
#                     else:
#                         print("Draft count element not found.")

                    
#                     await asyncio.sleep(1)
                    
#                     # Find and click the trash button
#                     trash_button = await page.waitForSelector('button.inline-flex svg.lucide-trash2')
#                     if trash_button:
#                         print("Found the Trash button.")
#                         await trash_button.click()
                    
#                     return text
                    
#             else:
#                 print("The words are less than 50")
#                 return None