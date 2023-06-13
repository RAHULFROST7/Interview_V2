import sys
import warnings
import timeit
import json
import time
import os
from math import ceil
from filelock import FileLock
sys.path.append(r"D:\Projects and codes\interview\resources")
from NLP_Transformer import Nlp_trans_SimCalc
from Transcriber import SpeechRecognizer
from NLP_engine import Nlp_eng_SimCalc
from Data_Base import QuestionManager

warnings.filterwarnings("ignore", category=DeprecationWarning)  # To remove deprecation warnings


def banner(text):
    # for logging
    print(f"!! {text} !!\n")


def append_to_json(question, ansScore,count):
    file_path = r"D:\Projects and codes\interview\resources\extinsion_interview\dump.json"
    result = {"question": question, "result": ansScore}
    lock_file = file_path + ".lock"

    while True:
        try:
            with FileLock(lock_file):
                with open(file_path, "r+") as file:
                    if count == '1':
                            file.truncate(0)
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

def check_file_presence(file_path):
    while not os.path.isfile(file_path):
        banner(f"Waiting for {file_path}")
        waiting_time = 5
        print(f"Waiting for {waiting_time} seconds...", end='')
        for i in range(waiting_time, -1, -1):
            print(f"\r{i} seconds remaining...{' ' * (len(str(waiting_time)) - len(str(i)))}", end='')
            time.sleep(1)
        banner("\n\nRetrying")


def connect_to_db(nQues):
    count = 1
    while True:
        try:
            count+=1
            answerDB = []
            obj = QuestionManager()
            order = obj.get_order()
            print("Order:", order)
            print("Nth question:", order[nQues])
            answerDB = obj.get_answers(question=order[nQues])
            print(answerDB)
            return answerDB, order
        except:
            banner("<#Network Error#>")
            waiting_time = 10
            print(f"Waiting for {waiting_time} seconds...", end='')
            for i in range(waiting_time, -1, -1):
                print(f"\r{i} seconds remaining...{' ' * (len(str(waiting_time)) - len(str(i)))}", end='')
                time.sleep(1)
            banner("\n\nRetrying")
            if count > 5 :
                banner(f"Fatal error on branch {count} 'can't convert text'")
                append_to_json(question="Fatal error due to DB or network error", ansScore=70)
                sys.exit()
            

def main():
    temp = sys.argv[1:]
    if temp == []:
        try:
            with open(r'D:\Projects and codes\interview\resources\extinsion_interview\count.txt', 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File 'count.txt' not found.")
        except IOError:
            print(f"Error reading file 'count.txt'.")
        banner(f"Fatal error on branch {content}")
        append_to_json(question="Fatal error due to command line argument", ansScore=70)
        sys.exit()
    else:
        count = str(temp[0])
        nQues = int(temp[0]) - 1

    banner(f"MAIN for audio_{count}.mp3")

    # Set the audio file name to check
    # audio_file = f"D:\\Projects and codes\\interview\\resources\\extinsion_interview\\out_{count}.mp3"
    """Test"""
    audio_file = r"D:\Projects and codes\interview\resources\extinsion_interview\test\out1arti.mp3"
    check_file_presence(audio_file)

    recognizer = SpeechRecognizer()
    givenAns = recognizer.convert_text(audio_file)
    print(givenAns)
    
    if givenAns is not None:
        banner("done converting text")
    else:
        banner(f"Fatal error on branch {count} 'can't convert text'")
        append_to_json(question="Did'nt answer the question or cant hear properly", ansScore=0)
        sys.exit()

    banner("Connecting to db")
    answerDB, order = connect_to_db(nQues)
    banner("Done fetching data from DB")

    banner("Comparing for score")
    
    obj_simx = Nlp_eng_SimCalc()
    ansScorex = obj_simx.getScore(answerDB, givenAns)

    obj_simy = Nlp_trans_SimCalc()
    ansScorey = obj_simy.calculate_similarity(answerDB, givenAns)

    print(f"X = {ansScorex}, Y = {ansScorey}")
    total_sim_score = ceil(0.4 * ansScorex + ansScorey * 0.6)
    print(f"Total score = {total_sim_score}")

    append_to_json(question=order[nQues], ansScore=total_sim_score,count=count)

    banner("completed execution")


if __name__ == "__main__":
    # print((timeit.timeit(main,number=1))/2)
    main()