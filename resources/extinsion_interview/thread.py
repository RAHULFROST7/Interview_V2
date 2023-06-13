import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import subprocess

# Read the count from the count.txt file
with open(r'D:\Projects and codes\interview\resources\extinsion_interview\count.txt', 'r') as f:
    count = int(f.read())
# if count > 5: 
#     '''change if'''
#     with open(r'D:\Projects and codes\interview\resources\extinsion_interview\count.txt', 'w') as f:
#         f.write(str(1))

# Run app.py as a subprocess with the current count
subprocess.Popen(["python", r"D:\Projects and codes\interview\resources\extinsion_interview\app.py", str(count)])

# Increment the count for the next run
count += 1

# Write the updated count back to the count.txt file

with open(r'D:\Projects and codes\interview\resources\extinsion_interview\count.txt', 'w') as f:
    f.write(str(count))