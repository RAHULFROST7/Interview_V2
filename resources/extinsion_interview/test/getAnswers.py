from pymongo import MongoClient
from typing import NewType

askedQuestion = NewType('askedQuestion',str)

def getAnswers(question : askedQuestion):
    
    client = MongoClient('mongodb+srv://webinterview:12345@cluster0.unj3vql.mongodb.net/main?retryWrites=true&w=majority')
    # print('connection successful');

    db = client['main']
    col = db['questions']

    myquery = {'question':question}

    data = col.find(myquery)

    for i in data:
        collected = list(i.values())[1:]
        
    return collected[1:]