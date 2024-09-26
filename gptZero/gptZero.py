import requests
from requests.exceptions import Timeout, RequestException

def check_with_gptzero(sentence, api_key):
    url = "https://api.gptzero.me/v2/predict/text"
    payload = {
        "document": sentence,
        "version": "",
        "multilingual": False
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parsing the response
        result = response.json()
        if 'documents' in result and len(result['documents']) > 0:
            doc = result['documents'][0]
            return doc
        else:
            print("No document data found in the response.")
            return {}
        
    except Timeout:
        print(f"Request to GPTZero timed out for sentence: {sentence}")
    except RequestException as e:
        print(f"Failed to check sentence with GPTZero: {e}")
    return {}


def collect_gptzero_scores(paragraph, api_key):
    document = {
        'text' : paragraph,
        'predicted_class': None,
        'gpt_score': None,
        'others_score': None,         
    }
    characters_count = len(paragraph)
    
    if characters_count > 250:
        try:
            score = check_with_gptzero(paragraph, api_key)
            class_probabilities = score.get('class_probabilities', {})
            predicted_class = score.get('predicted_class', 0)
            probabilities = class_probabilities.get(predicted_class, 0) * 100  
            
            print("predicted_class:", predicted_class, "\nprobabilities:", probabilities)
            
            document['predicted_class'] = predicted_class
            document['gpt_score'] = probabilities
            document['others_score'] = score
            
        except Exception as e:
            print("Error occurred during humanization:", e)
    
    else:
        document['predicted_class'] = "Too short to predict"
    
    return document


