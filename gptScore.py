from database.connections import *
from gptZero.gptZero import collect_gptzero_scores
import time

def gptZero_process(db, api_key):
    try:
        documents = fetch_humanized_texts_for_gptZero(db)
        docs = list(documents)
        if not documents:
            print("========No More Data to Process=========")
            return False

        max_humanized_texts = max(len(doc['humanized_text']) for doc in docs)
        paragraphs = []
        print(f"No. of paragraphs will be : {max_humanized_texts}")
        
        
        for i in range(max_humanized_texts):    
            text = ""
            for doc in docs:
                text="".join([text,doc['humanized_text'][i]]).strip()
            
            print("the text is formed..........!!")
            paragraphs.append(text)
        
        results = []

        # Fetch GPTZero scores for each paragraph
        for idx, text in enumerate(paragraphs):
            print(f"\nProcessing Paragraph {idx + 1}:\n{text}")
            try:
                score = collect_gptzero_scores(text, api_key)
                results.append(score)
            except Exception as e:
                print(f"Error collecting GPTZero score for paragraph {idx + 1}: {e}")

        store_paragraph_with_gptscore(db, results)
        return True

    except Exception as e:
        print(f"Error processing on gptScore Process: {e}")
        return False

def main():
    db = connect_to_mongo()
    api_key = "836c886632d24c92a32036972ccba92b"
    retry = 0
    max_retries = 5
    sleep_time = 24*60
    
    while True:
        try:
            success = gptZero_process(db, api_key)     
            if not success:              
                print("\n========No More Data to Process=========")
                if retry < max_retries:
                    retry += 1
                    print(f"GPTZero process is failed. Retrying in {sleep_time} seconds... (Attempt {retry}/{max_retries})\n")
                    time.sleep(sleep_time)
                else:
                    print(f"\n\t\t\t\t\t\t\t!X_X!.....GPTZero process is terminating......!X_X!\n")
                    break
            else:
                retry = 0 
                print("[INFO] GPTZero process completed successfully. Running again for Next Data...")
        
        except Exception as e:
            print(f"[ERROR] Unexpected error in GPTZero process: {e}")
            break

if __name__ == "__main__":
    
    main()
