from pymongo import MongoClient

class QuestionManager:
    def __init__(self):
        pass

    def get_answers(self,question):
        
        connection_string = 'mongodb+srv://webinterview:12345@cluster0.unj3vql.mongodb.net/main?retryWrites=true&w=majority'
        database_name = 'main'
        collection_name = 'questions'
        collected = []
        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]

        myquery = {'question': question}
        
        data = collection.find(myquery)

        for i in data:
            collected = list(i.values())[1:]

        return collected[1:]

    def get_order(self,connection_string = "mongodb+srv://interview:12345@cluster0.1ahe7l7.mongodb.net/interview?retryWrites=true&w=majority",database_name = "interview",collection_name = "questions"):
        
        client = MongoClient(connection_string)
        db = client[database_name]
        collection = db[collection_name]

        docs = collection.find()

        data = []
        for doc in docs:
            data.append(doc['ques'])
            
        return data[0]
