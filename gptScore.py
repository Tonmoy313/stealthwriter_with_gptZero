from database.connections import *
from gptZero.gptZero import collect_gptzero_scores
import time

def process_humanized_texts(db, api_key):
    try:
        docs = fetch_humanized_texts_for_gptZero(db)
        if not docs:
            print("========No More Data to Process=========")
            return False

        max_humanized_texts = max(len(doc['humanized_text']) for doc in docs)
        paragraphs = []

        # Create paragraphs from humanized texts
        for i in range(max_humanized_texts):
            paragraph = []
            for doc in docs:
                try:
                    paragraph.append(doc['humanized_text'][i])
                except IndexError:
                    print(f"Index {i} out of range for document {doc['_id']}, skipping.")
            paragraphs.append(" ".join(paragraph).strip())

        print("The number of paragraphs created:", len(paragraphs))
        results = []

        # Fetch GPTZero scores for each paragraph
        for idx, text in enumerate(paragraphs):
            print(f"Processing Paragraph {idx + 1}: {text}")
            try:
                score = collect_gptzero_scores(text, api_key)
                results.append(score)
            except Exception as e:
                print(f"Error collecting GPTZero score for paragraph {idx + 1}: {e}")

        store_paragraph_with_gptscore(db, results)
        return True

    except Exception as e:
        print(f"Error processing humanized texts: {e}")
        return False

def main():
    db = connect_to_mongo()
    api_key = "836c886632d24c92a32036972ccba92b"
    retry = 0
    while True:
        try:
            success = process_humanized_texts(db, api_key)
            if not success:
                if retry < 5 :
                    print("There is no data to be proccessed for gptZero")
                    time.sleep(20)
                    retry +=1
                    
                else:
                    print("!!..THe GptScore Processing is terminated....!!")
                    break
        except Exception as e:
            print(f"Unexpected error for gptZero: {e}")
            break

if __name__ == "__main__":
    main()
