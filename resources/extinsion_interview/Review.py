from transformers import pipeline
from time import sleep
import pymongo

class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", revision="af0f99b")


    def analyze_sentiment(self, text):
        result = self.classifier(text, truncation=True)[0]
        sentiment = result['label']
        score = result['score']
        positive_prob = score if sentiment == 'POSITIVE' else 1 - score
        negative_prob = 1 - positive_prob

        return sentiment, positive_prob, negative_prob
            
    def push_to_Db(self,data):
        
        while True:
            try:
                # Establish a connection to the MongoDB server
                client = pymongo.MongoClient("mongodb+srv://webinterview:12345@cluster0.unj3vql.mongodb.net/?retryWrites=true&w=majority")

                # Access the desired database
                db = client["main"]

                # Access the desired collection
                collection = db["Review"]

                # Insert the data into the collection
                collection.insert_one(data)

                print("Data successfully pushed to MongoDB.")
                break
            
            except Exception as error:
                print("Error while connecting to MongoDB")
                print("retrying in 10 seconds....")
                sleep(10)
    
def main():
    
    analyzer = SentimentAnalyzer()
    
    file_path = r"D:\Projects and codes\interview\resources\extinsion_interview\review.txt"
    while True:
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                if text != "":
                    print("Got the text")
                    break
                else:
                    print("Waiting for text")
                    sleep(5)
                    
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            sleep(5)
            
        
    sentiment, positive_prob, negative_prob = analyzer.analyze_sentiment(text)

    data = {
        "sentiment":sentiment,
        "positive_prob":positive_prob,
        "negative_prob":negative_prob,
        "text":text
    }
    
    print("Review:", sentiment)
    # print("Positive probability:", positive_prob)
    # print("Negative probability:", negative_prob)
    analyzer.push_to_Db(data)
    
if __name__=="__main__":
    main()