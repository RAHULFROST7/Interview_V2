import os
from time import sleep
def deleteFiles():
    count = 1
    with open(r'D:\Projects and codes\interview\resources\extinsion_interview\count.txt', 'w') as f:
        f.write(str(count))
    print("Replaced text file as:",count)
    
    # Create stop recording file
    print("Terminating Iris_detection.py")
    with open('stop_recording', 'w') as f:
        f.write('')
    
    while True:
        # print("In while")
        path = f"D:\\Projects and codes\\interview\\resources\\extinsion_interview\\out_{count}.mp3"
        if os.path.isfile(path):
            sleep(10)
            os.remove(path)
            print(f"Removed audio file out_{count}.mp3")
            count+=1
        else:
            print("Delete.py ran succesfully or the path does not exit")
            break


if __name__ == "__main__":
    deleteFiles()


