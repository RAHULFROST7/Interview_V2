"""_summary_ 

    remains or old structure of 'Transcriber.py'

   _Reason_
    
    slow and clumsy
"""

# import re
import torch
import whisper
from typing import NewType
import warnings
import timeit
from functools import lru_cache
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# path_of_audio = NewType('path_of_i_th_audio',str)

def banner(text):
    # """Display a message when the script is working in the background"""
    print(f"# {text} #\n")


def check_device():
    
    # """Check CUDA availability."""
    if torch.cuda.is_available() == 1:
        device = "cuda"
        
    else:
        device = "cpu"
        
    # return device
    return "cpu"

# """Get speech recognition model."""
# model_name = input("Select speech recognition model name (tiny, base, small, medium, large): ")
# @lru_cache(maxsize=None)  # Decorator to enable caching
def load_model(model_name):
    return whisper.load_model(model_name, device=check_device())

def convertText(AUDIOFILE):
    
    # list_temp=[]
    warnings.filterwarnings("ignore", category=UserWarning)
    #choose a mode defaulted
    """tiny"""

    model_name = "base"

    banner("Transcribing texts")
    model = load_model(model_name)
        
    # for i in range(0,len(AUDIOFILE)):
        
    result = model.transcribe(AUDIOFILE)
    warnings.resetwarnings()
    # print("Result: ",result["text"])
    return result["text"]
        
   
    
    # return list_temp
    
# measure execution time of my_function
# print(convertText(r"D:\Projects and codes\interview\resources\extinsion_interview\out1.mp3"))


"""_summary_ 

    remains or old structure of 'NLP_Transformer.py'

   _Reason_
    
    clumsy , unreadable
"""

from sentence_transformers import SentenceTransformer,util
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
from time import sleep
import time
from math import ceil
import random


def calculate_similarity(sentences_list,sentence):
    # Encode sentences and obtain embeddings
    """ Can even use 'bert-base-nli-stsb-mean-tokens' or 'bert-base-nli-max-tokens'"""
    model = SentenceTransformer('bert-base-nli-mean-tokens')        #180 97 -366 218 -124 -309
    # model = SentenceTransformer('bert-base-nli-stsb-mean-tokens') #177 79 -384 214 -108 -352
    # model = SentenceTransformer('bert-base-nli-max-tokens')       #149 65 -307 157 -109 -277  """ Reject this model """

    sentence_embeddings = model.encode([sentence])
    sentences_embeddings = model.encode(sentences_list)
    
    similarity_score = []

    for embedding in sentences_embeddings:
        # Calculate cosine similarity
        cos_similarity = util.pytorch_cos_sim(sentence_embeddings[0], embedding)
        similarity_score_cos = ceil(cos_similarity.item() * 100) if  ceil(cos_similarity.item() * 100) > 0 else 0

        # Calculate Euclidean distance
        euclidean_distance = euclidean(sentence_embeddings[0], embedding)
        similarity_score_euc = ceil(calculate_similarity_score(abs(euclidean_distance)))
        
        cosi_similarity = cosine_similarity([sentence_embeddings[0]], [embedding])[0][0]
        cosine_similarity_score = (ceil(101 * cosi_similarity)) if cosi_similarity > 0 else 0

        # Combine the similarity scores (adjust the weights as desired)
        similarity_score.append(ceil(0.15 * similarity_score_cos + 0.70 * similarity_score_euc + 0.15 * cosine_similarity_score))

    # print(similarity_score)
    return max(similarity_score)    
    

def calculate_similarity_score(distance):
    # Normalize the distance between 0 and 1
    min_distance = 0.0  # Minimum possible distance
    max_distance = 10.0  # Maximum possible distance

    normalized_distance = (distance - min_distance) / (max_distance - min_distance)

    # Transform the normalized distance to a similarity score between 0 and 100
    similarity = 100 * (1 - normalized_distance) * 3.3
    # similarity = 100 * (1 - normalized_distance)

    return similarity if similarity > 0 and similarity < 100 else random.randint(97,100) if similarity > 100 else 0
    # return similarity

# def main():
    
#     # sentence1 = 'Artificial Intelligence (AI) refers to the ability of machines to perform tasks that typically require human-like intelligence, such as learning, reasoning, problem-solving, perception, and natural language processing.'
#     # sentence2 = "Artificial intelligence is a branch of computer science and engineering that focuses on developing intelligent machines capable of performing quantitative tasks that are traditionally associated with human beings. Artificial intelligence (AI) refers to the development of computer systems that possess the ability to perform tasks that typically require human intelligence. It encompasses a wide range of techniques and methodologies aimed at creating intelligent machines capable of learning, reasoning, problem-solving, perceiving, and processing natural language. AI systems are designed to emulate human-like cognitive abilities and make autonomous decisions or take actions based on data and patterns. By leveraging algorithms, statistical models, and large datasets, AI enables machines to recognize patterns, make predictions, adapt to changing conditions, and interact with humans in a natural and intelligent manner. AI has applications in various domains, including robotics, healthcare, finance, transportation, and many others, where it has the potential to revolutionize industries, improve efficiency, and enhance decision-making processes."
#     sentence1 = ["Machine learning (ML) is a subset of AI that deals with the development of algorithms and models that enable computers to learn and make predictions based on data. It involves training computers on large datasets to recognize patterns and make informed decisions without being explicitly programmed. ML has applications in areas like image and speech recognition, recommendation systems, and fraud detection, where it plays a vital role in automating tasks and extracting meaningful insights from data.",'Machine learning (ML) is a subset of artificial intelligence (AI) that focuses on the development of algorithms and models that enable computers to learn and make predictions based on data. It involves training machines on large datasets to recognize patterns, extract insights, and make informed decisions without being explicitly programmed.']
#     # sentence2 = "Mount Everest is the highest peak in the world, located in the Himalayas. It stands at an elevation of approximately 8,848 meters (29,029 feet) above sea level. Climbing Mount Everest is a challenging and dangerous feat that requires extensive preparation, physical endurance, and mountaineering skills. Many climbers attempt to conquer Everest each year, braving extreme weather conditions and navigating treacherous terrain. The summit offers breathtaking views and a sense of accomplishment for those who reach the top."
#     # sentence2 = ""
#     sentence2 = "Machine Learning has numerous applications across various domains, including image and speech recognition, natural language processing, recommendation systems, and fraud detection. It has revolutionized industries and transformed the way businesses operate. With ML, companies can automate tasks, improve efficiency, and gain valuable insights from their data."
#     # sentence2 = 'Machine learning (ML) is a subset of artificial intelligence (AI) that focuses on the development of algorithms and models that enable computers to learn and make predictions based on data. It involves training machines on large datasets to recognize patterns, extract insights, and make informed decisions without being explicitly programmed.'
#     # sentence1 = "My name is Rahul"
#     # sentence2 = "Rahul is not my name"
#     calculate_similarity(sentence1, sentence2)
#     # """Succesfull test"""


# if __name__ == "__main__":
#     st = time.time()
#     main()
#     ed = time.time()
    
#     tot = ed - st
    
#     print(f"Toatal time = {tot}")
 
"""_summary_ 

remains or old structure of 'NLP_engine.py'

_Reason_

clumsy , unreadable
"""
 
import spacy
import nltk
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import numpy as np
from math import ceil , floor
import warnings
from typing import NewType
nlp = spacy.load('en_core_web_lg')
actualAnswer = NewType('actualAnswer' ,list) 
givenAnswer = NewType('givenAnswer' ,str)

def getScore( sentence1 : actualAnswer , sentence2 : givenAnswer ):
    #                       list[n]                 string
    
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    def preprocess_sentence(text : str):
            
            text = text.lower()
            text = text.translate(str.maketrans("", "", string.punctuation))
            stop_words = set(stopwords.words("english"))
            words = text.split()
            words = [w for w in words if w not in stop_words]
            
            return " ".join(words)
        
        
    # lenS1 = len(sentence1)
    # lenS2 = len(sentence2)
    
    # if((lenS1 and lenS2 != 0) and ((lenS1 * 1/7) < lenS2)):
    
    processed_sentence2 = preprocess_sentence(sentence2)
    score_list = []
    tokens2 = set(nltk.word_tokenize(sentence2.lower()))
    
    
    for i in range(0,len(sentence1)):
        
        # print("Gets in")
        processed_sentence1 = preprocess_sentence(sentence1[i])
        final_score = 0
            
        # print(nlp.meta['name'], '\n')
        weighted_score = 0

        # Compute Spacy similarity score
        doc1 = nlp(processed_sentence1)
        doc2 = nlp(processed_sentence2)
        spacy_similarity_score = 0
        spacy_similarity_score = doc1.similarity(doc2)
        

        # Compute TF-IDF vector representation for each sentence
        vectorizer = TfidfVectorizer()
        sentence1_tfidf = vectorizer.fit_transform([processed_sentence1])
        sentence2_tfidf = vectorizer.transform([processed_sentence2])


        # Compute cosine similarity score using TF-IDF vectors
        cosine_similarity_score = 0
        cosine_similarity_score = cosine_similarity(sentence1_tfidf, sentence2_tfidf)[0][0]
        
        
        try:
            
            tokens1 = word_tokenize(processed_sentence1)
            tokens2 = word_tokenize(processed_sentence2)
                
            # create word embeddings for each string
            model = gensim.models.Word2Vec([tokens1, tokens2], min_count=2)
            word_vectors = {word: model.wv[word] for word in model.wv.index_to_key}
                
            # calculate the average vector for each string
            vector1 = np.mean([word_vectors[word] for word in tokens1 if word in word_vectors], axis=0)
            vector2 = np.mean([word_vectors[word] for word in tokens2 if word in word_vectors], axis=0)
                
            # calculate cosine similarity between the vectors
            sim_score = 0
            sim_score = cosine_similarity([vector1], [vector2])[0][0]
            # print("ends within try")
            
        except:
            
            sim_score = 0
            # print("except")
            sim_score = weighted_score


        tokens1 = set(nltk.word_tokenize(sentence1[i].lower()))

        jaccard_similarity_score = 0
        jaccard_similarity_score = len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))


        # Weighted average of the similarity scores
        weighted_score = (0.5 * spacy_similarity_score) + (0.3 * jaccard_similarity_score) + (0.2 * cosine_similarity_score)
        

        # Compute the average similarity score
        
        average_similarity_score = 0
        average_similarity_score = spacy_similarity_score * .15 + ( jaccard_similarity_score + cosine_similarity_score + ( weighted_score + sim_score ) * .15 ) / 2
        final_score = ceil(average_similarity_score * 100)
        # print(final_score)
        score_list.append(final_score)
    # print(score_list)

    result = max(score_list)
    return (np.random.randint(8,30)) if result < 50 and result > 10 else ((np.random.randint(95,100)) if result > 100 else (floor(result*1.15) if (result <75 and result > 60) else (floor(result * 0.6) if (result < 70 and result > 50) else ( 0 if result < 0 else result))))
        
        # else:
        #     return 0


# print(getScore(['Machine Learning has numerous applications across various domains, including image and speech recognition, natural language processing, recommendation systems, and fraud detection. It has revolutionized industries and transformed the way businesses operate. With ML, companies can automate tasks, improve efficiency, and gain valuable insights from their data.'],"Machine learning (ML) is a subset of AI that deals with the development of algorithms and models that enable computers to learn and make predictions based on data. It involves training computers on large datasets to recognize patterns and make informed decisions without being explicitly programmed. ML has applications in areas like image and speech recognition, recommendation systems, and fraud detection, where it plays a vital role in automating tasks and extracting meaningful insights from data."))





import sys
sys.path.append(r'D:\Projects and codes\interview\resources') #Important for using resources from resources!!!!

# Imports 
from NLP_Transformer import Nlp_trans_SimCalc
from Transcriber import SpeechRecognizer
from NLP_engine import Nlp_eng_SimCalc
from Data_Base import QuestionManager
from filelock import FileLock
from math import ceil
import warnings
import timeit
import json
import time
import os

warnings.filterwarnings("ignore", category=DeprecationWarning) #To remove depereciation warnings


def banner(text):
    # for loging
    print(f"!! {text} !!\n")
    
def append_to_json(question, ansScore):
    file_path = r"D:\Projects and codes\interview\resources\extinsion_interview\dump.json"#change path later accordingly 
    # file_path = r"dump.json"
    result = {"question": question, "result": ansScore}
    lock_file = file_path + ".lock"

    while True:
        
        try:
            with FileLock(lock_file):
                with open(file_path, "r+") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = {"results": []}
                    data["results"].append(result)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
            break
        except PermissionError:
            print(f"File {file_path} is locked. Waiting for a second...")
            time.sleep(1)


def main():
    
    temp = sys.argv[1:]
    # print(temp)
    if temp == []:
        try:
            with open(r'D:\Projects and codes\interview\resources\extinsion_interview\count.txt', 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File 'count.txt' not found.")
        except IOError:
            print(f"Error reading file 'count.txt'.")
        banner(f"Fatal error on branch {content}")
        append_to_json(question="Fatal error due to command line argument",ansScore=70)
        sys.exit()
    else:
        count = str(temp[0])
        nQues = int(temp[0])-1

    banner(f"MAIN for audio_{count}.mp3")
    
    # Set the audio file name to check
    # audio_file = f"D:\\Projects and codes\\interview\\resources\\extinsion_interview\\out_{count}.mp3"
    audio_file = r"D:\Projects and codes\interview\resources\extinsion_interview\test\out1arti.mp3"

    # Continuously check for the presence of the audio file
    while True:
        if os.path.isfile(audio_file):
            recognizer = SpeechRecognizer()
            givenAns = recognizer.convert_text(audio_file)
            print(givenAns)
            banner("done converting text") if givenAns != None else banner("Fatal error cant convert text")
            break
        else:
            banner("<#Waiting for Audio_{count}.mp3#>")
            waiting_time = 5
            print(f"Waiting for {waiting_time} seconds...", end='')
            for i in range(waiting_time, -1, -1):
                print(f"\r{i} seconds remaining...{' '*(len(str(waiting_time))-len(str(i)))}", end='')
                time.sleep(1)
            banner("\n\nRetrying")
            

    banner("Connecting to db")
    while True:
        
        try:
            answerDB = []
            obj = QuestionManager()
            order = obj.get_order()
            print("Order : ",order,"\n\nNth question : ",order[nQues])
            answerDB = obj.get_answers(question = order[nQues])
            print(answerDB) 
            break
         
        except:
            banner("<#Network Error#>")
            waiting_time = 20
            print(f"Waiting for {waiting_time} seconds...", end='')
            for i in range(waiting_time, -1, -1):
                print(f"\r{i} seconds remaining...{' '*(len(str(waiting_time))-len(str(i)))}", end='')
                time.sleep(1)
            banner("\n\nRetrying")
            
    banner("Done fetching data from DB")
        
    banner("Comparing for score")
    
    
    obj_simx = Nlp_eng_SimCalc()
    ansScorex = obj_simx.getScore(answerDB,givenAns)
    
    
    obj_simy = Nlp_trans_SimCalc()
    ansScorey = obj_simy.calculate_similarity(answerDB,givenAns)
    
    
    print("X =", ansScorex, "Y =", ansScorey)
    
    total_sim_score = ceil(.4 * ansScorex + ansScorey * .6)
    
    print(f"Total score = {total_sim_score}")
    
    append_to_json(question=order[nQues],ansScore=total_sim_score)
    
    banner("completed execution")
    

if __name__ == "__main__":
    # main()
    print("Time taken = ",(timeit.timeit(main,number=2))/2)