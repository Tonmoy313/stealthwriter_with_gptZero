# For multiprocessing

import multiprocessing
import subprocess
import time 

def run_stealth_writer():
    print("Stealth Writer Process Running")
    subprocess.run(['python', 'stealthWriter.py'])

def run_gpt_score():
    print("GptZero Process Running")
    while True:
        result = subprocess.run(['python', 'gptScore.py'])
        if result.returncode == 0:
            print("GptZero Process Completed Successfully")
            break
        else:
            print("No data found for GptZero, waiting to retry...")
            time.sleep(60)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_stealth_writer)
    p2 = multiprocessing.Process(target=run_gpt_score)

    # Start the processes
    p1.start()
    p2.start()

    p1.join()
    p2.join()
