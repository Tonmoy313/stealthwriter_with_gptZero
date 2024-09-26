from pymongo import MongoClient, errors
from bson.objectid import ObjectId

def connect_to_mongo():
    try:
        # CONNECTION_STRING = "mongodb://root:1234@localhost:27018"
        CONNECTION_STRING = "mongodb+srv://abdullahalmahmudcse007:5s3XzQhtxtsA5zGt@cluster0.q78iz.mongodb.net"
        
        client = MongoClient(CONNECTION_STRING)
        
        db = client['bypass']
        print("Successfully connected to MongoDB.")
        return db
    
    except errors.ConnectionError as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# For StealthWriter
def fetch_text_form_scrapingDb(db):
    try:
        collection = db['demo'] 
        document = collection.find_one({"processed": {"$ne": True}})
        if document:
            print("Text fetched successfully.")
            return document
        else:
            print("No text found to humanize.")
            return None
    
    except errors.PyMongoError as e:
        print(f"Error fetching text from MongoDB: {e}")
        return None


def store_humanized_text(db, documents, scraping_data_id):
    try:
        collection = db['tbl_humanizingData']
        result = collection.insert_many(documents)
        if result:
            collection2 = db['demo']
            collection2.update_one({"_id": scraping_data_id}, {"$set": {"processed": True}})
            print("Done stealthWirting Process for id:", scraping_data_id)
        print(f"Humanized texts stored successfully")
        return result
        
    except errors.PyMongoError as e:
        print(f"Error storing humanized texts in MongoDB: {e}")
        return None


# For gptZero 

def fetch_humanized_texts_for_gptZero(db):
    try:
        collection = db['demo']
        document = collection.find_one({"processed": True, "processed_gptZero": {"$ne": True}})
        if document:
            print("Text fetched successfully for GPTZero processing.")
            collection.update_one({"_id": document["_id"]}, {"$set": {"processed_gptZero": True}})
            collection1 = db['tbl_humanizingData']
            cursor = collection1.find({"scraping_id": document["_id"]}).sort("sentence_no", 1)
            return cursor
        else:
            print("No text available for GPTZero processing.")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None


def store_paragraph_with_gptscore(db, documents):
    try:
        collection = db['tbl_gptScore']
        result = collection.insert_many(documents)
        print(f"Paragraph with GPT score stored successfully")
        return result.inserted_ids  
        
    except errors.PyMongoError as e:
        print(f"Error storing paragraph with GPT score in MongoDB: {e}")
        return None

