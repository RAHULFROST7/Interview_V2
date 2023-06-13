# # # # import re
# # # import torch
# # # import whisper
# # # from typing import NewType
# # # import warnings
# # # import timeit

# # # # path_of_audio = NewType('path_of_i_th_audio',str)

# # # def banner(text):
# # #     # """Display a message when the script is working in the background"""
# # #     print(f"# {text} #\n")


# # # def check_device():
    
# # #     # """Check CUDA availability."""
# # #     if torch.cuda.is_available() == 1:
# # #         device = "cuda"
        
# # #     else:
# # #         device = "cpu"
        
# # #     return device

# # # # """Get speech recognition model."""
# # # # model_name = input("Select speech recognition model name (tiny, base, small, medium, large): ")

# # # def convertText(AUDIOFILE : list):
    
# # #     list_temp=[]
# # #     warnings.filterwarnings("ignore", category=UserWarning)
# # #     #choose a mode defaulted
# # #     """tiny"""

# # #     model_name = "base"

# # #     banner("Transcribing texts")
# # #     model = whisper.load_model(model_name, device=check_device())
# # #     # Quantize the model
    
# # #     # quantized_model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

        
# # #     for i in range(0,len(AUDIOFILE)):
        
# # #         result = model.transcribe(AUDIOFILE[i])
        
# # #         # print("Result: ",result["text"])
# # #         list_temp.append(result["text"])
        
# # #     warnings.resetwarnings()
    
# # #     return list_temp
    
# # # # Define the audio files to transcribe
# # # audio_files = [r"D:\Projects and codes\interview\resources\test_audio_e_airport.mp3",r"D:\Projects and codes\interview\resources\test_audio_e_spanish.mp3",r"D:\Projects and codes\interview\resources\test_audio_e_time.mp3"]

# # # # Measure execution time
# # # execution_time = timeit.timeit(lambda: convertText(audio_files), number=1)

# # # # Print the transcriptions and execution time
# # # # transcriptions = convertText(audio_files)
# # # # print("Transcriptions:")
# # # # for transcription in transcriptions:
# # # #     print(transcription)
# # # print(f"\nExecution time: {execution_time:.6f} seconds")

# # import torch
# # import whisper
# # from functools import lru_cache
# # from multiprocessing import Manager, Process
# # import warnings
# # def banner(text):
# #     print(f"# {text} #\n")

# # def check_device():
# #     if torch.cuda.is_available() == 1:
# #         device = "cuda"
# #     else:
# #         device = "cpu"
# #     return device

# # @lru_cache(maxsize=None)
# # def load_model(model_name):
# #     return whisper.load_model(model_name, device=check_device())

# # def convertText(AUDIOFILE, model):
# #     list_temp = []
# #     warnings.filterwarnings("ignore", category=UserWarning)

# #     banner("Transcribing texts")
# #     result = model.transcribe(AUDIOFILE)
# #     list_temp.append(result["text"])

# #     warnings.resetwarnings()
# #     return list_temp

# # def parallel_convertText(AUDIOFILE, model):
# #     manager = Manager()
# #     result_list = manager.list()
# #     processes = []

# #     for audio in AUDIOFILE:
# #         p = Process(target=convertText, args=(audio, model, result_list))
# #         processes.append(p)
# #         p.start()

# #     for p in processes:
# #         p.join()

# #     return list(result_list)

# # if __name__ == '__main__':
# #     model_name = "base"
# #     model = load_model(model_name)
# #     audio_files = [
# #         r"D:\Projects and codes\interview\out_1.mp3",
# #         r"D:\Projects and codes\interview\out_2.mp3",
# #         r"D:\Projects and codes\interview\out_3.mp3"
# #     ]

# #     results = parallel_convertText(audio_files, model)
# #     print(results)
# import json
# from filelock import FileLock

# def append_to_json(result):
#     output_file = r"D:\Projects and codes\interview\resources\extinsion_interview\result.json"

#     # Acquire file lock before appending to the JSON file
#     with FileLock(output_file).acquire():
#         with open(output_file, "r") as file:
#             data = json.load(file)
#             data["results"].append(result)
#             file.seek(0)  # Move the file pointer to the beginning
#             json.dump(data, file, indent=4)  # Write the updated data
#             file.truncate()  # Truncate the file to remove any remaining content

# result = {
#     "question": "What is Ml",
#     "result": "-1"
# }

# append_to_json(result)

