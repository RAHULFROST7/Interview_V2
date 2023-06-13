from pymongo import MongoClient
import datetime
from pydub import AudioSegment



def sliceAudio(path:str):

    # replace the connection string and database/collection names with your own values
    connection_string = "mongodb+srv://interview:12345@cluster0.1ahe7l7.mongodb.net/interview?retryWrites=true&w=majority"
    database_name = "interview"
    collection_name = "timestamps"

    # create a MongoClient object and connect to your MongoDB instance
    client = MongoClient(connection_string)
    # print("got 1")
    # get the database
    db = client[database_name]
    # print("got 2")
    # get the collection
    collection = db[collection_name]
    # print("got 3")
    # you can now perform operations on the collection
    # for example, find all documents in the collection
    num_documents = collection.count_documents({})
    # for document in collection.find():
    #     print(document['start'])
        # timestamp1 = datetime.datetime.strptime(timestamp1_str, "%Y-%m-%d %H:%M:%S")
        # timestamp2 = datetime.datetime.strptime(timestamp2_str, "%Y-%m-%d %H:%M:%S")
    timestamps=[]
    # print("got 3")
    for i in range(num_documents):
        timestamp1_str = collection.find()[i]['start']
        timestamp2_str = collection.find()[i]['end']
        timestamp1 = datetime.datetime.strptime(timestamp1_str, "%Y-%m-%d %H:%M:%S")
        timestamp2 = datetime.datetime.strptime(timestamp2_str, "%Y-%m-%d %H:%M:%S")
        time_diff = timestamp1 - timestamp2
        timestamps.append(int(abs(time_diff.total_seconds())))

    # print("got 4")
    # audio = audio = AudioSegment.from_file(path, format="mp3")
    audio = AudioSegment.from_wav(path)
    # print("got 5")
    print(timestamps,"\n")
    
    # test data
    # comment if you found this uncommented
    # timestamps = [50,57,45]
    # print(timestamps)
    # test data
    
    start_time = 0
    path_list = []
    for i, duration in enumerate(timestamps):
        end_time = start_time + duration
    
        
        sliced_audio = audio[ start_time * 1000 : end_time * 1000 ]

        # Export the sliced audio to a file
        sliced_audio.export(f"D:\\Projects and codes\\interview\\resources\\sliced_audio_{i+1}.mp3", format="mp3")
        path_list.append(f"D:\\Projects and codes\\interview\\resources\\sliced_audio_{i+1}.mp3")
        start_time = end_time
    # print("got 6")
    
    
    collection_name = "questions"

    # create a MongoClient object and connect to your MongoDB instance
    # client = MongoClient(connection_string)

    # get the database
    db = client[database_name]

    # get the collection
    collection = db[collection_name]

    # you can now perform operations on the collection
    # for example, find all documents in the collection

    # fetch all documents from the collection
    docs = collection.find()

    # print each document
    for doc in docs:
        data = (doc['ques'])
    
    print(f"{list(data)}\n")

    return path_list,list(data)

# print(sliceAudio(r"D:\Projects and codes\interview\resources\extenion_interview\out.wav"))
