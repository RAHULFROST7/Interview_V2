import sys

sys.path.append(r'D:\Projects and codes\interview\resources')


from Transcriber import convertText
from NLP_engine import getScore
from slicer import sliceAudio
from pymongo import MongoClient
from typing import NewType
import json
import time
# from TrainModel import sentimentAnalyzer

def banner(text):
    # for loging
    print(f"!! {text} !!\n")
    
def writeData(data):

    # data = {"Result 1": 23, "Result 2": 30, "Result 3": 54}

    # Open a file for writing
    with open(r"D:\Projects and codes\interview\resources\extinsion_interview\result.json", "w") as f:
        # Use json.dump() to write the data to the file
        json.dump(data, f)

askedQuestion = NewType('askedQuestion',str)

def getAnswers(question : askedQuestion):
    
    collected = []
    client = MongoClient('mongodb+srv://webinterview:12345@cluster0.unj3vql.mongodb.net/main?retryWrites=true&w=majority')
    # print('connection successful');

    db = client['main']
    col = db['questions']

    myquery = {'question':question}

    data = col.find(myquery)

    for i in data:
        collected = list(i.values())[1:]
        
    return collected[1:]

# def getOrder():

#     connection_string = "mongodb+srv://interview:12345@cluster0.1ahe7l7.mongodb.net/interview?retryWrites=true&w=majority"
#     database_name = "interview"
#     collection_name = "questions"

#     # create a MongoClient object and connect to your MongoDB instance
#     client = MongoClient(connection_string)

#     # get the database
#     db = client[database_name]

#     # get the collection
#     collection = db[collection_name]

#     # you can now perform operations on the collection
#     # for example, find all documents in the collection

#     # fetch all documents from the collection
#     docs = collection.find()

#     # print each document
#     for doc in docs:
#         data = (doc['ques'])
    
#     return list(data)

def main():
    
    
    banner("MAIN")
    
    path = r"D:\Projects and codes\interview\resources\extinsion_interview\out.wav"

    banner("Spliting audio")
    
    list_paths,order = sliceAudio(path=path)
        
    banner('Done')
    
    banner("converting audio to txt")
        
    givenAnsDB = convertText(list_paths)
        
    # print(givenAnsDB)
    
    banner("Done") if len(givenAnsDB) == len(list_paths) else banner("Fatal error : Can't convert given part of audio")
        
    while True:
        
        try:
        
            banner("Getting answers")
            answerDB = []
            # questionsDB = ["What is machine learning?","What is Artificial Intelligence?","What is data science?","What is deep learning?","What is data structures?"]
            # questionsDB = ["what is machine learning","what is artificial intelligence","what is data science","what is deep learning","what is data structure"]
            
            for i in range(0,len(order)):

                temp_list = getAnswers(order[i])
                
                answerDB.append(temp_list)
                
            # print(answerDB) 
    
            break 
        except:
            banner("<#Network Error#>")
            waiting_time = 20
            print(f"Waiting for {waiting_time} seconds...", end='')
            for i in range(waiting_time, -1, -1):
                print(f"\r{i} seconds remaining...{' '*(len(str(waiting_time))-len(str(i)))}", end='')
                time.sleep(1)
            banner("Retrying")
            
    banner("Done")
        

    banner("Comparing for score")
    
    ansScores = []
    for k in range(0,(len(answerDB))):
        
        # print(answerDB[k],givenAnsDB[k])
        temp = getScore(answerDB[k],givenAnsDB[k])

        ansScores.append(temp)
    print(ansScores)
    total = 0
    
    for l in range(0,len(ansScores)):
        total += ansScores[l]
        
    totalScore = total/len(ansScores)
    print(f"\nAverage Score is {totalScore}\n")

    data = {"results": [{"question":order[0],"result": ansScores[0]},{"question":order[1],"result": ansScores[1]},{"question":order[2],"result": ansScores[2]},{"question":order[3],"result": ansScores[3]},{"question":order[4],"result": ansScores[4]}]}
    writeData(data)         
    banner("completed execution")
    

if __name__ == "__main__":

    main()
    