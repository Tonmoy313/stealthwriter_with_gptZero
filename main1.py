# For Multi threading

import threading
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
            print("*****GptZero Process Completed Successfully****")
            break
        else:
            print("No data found for GptZero, waiting to retry...")
            time.sleep(60)

if __name__ == "__main__":
    # Create threads
    t1 = threading.Thread(target=run_stealth_writer)
    t2 = threading.Thread(target=run_gpt_score)

    # Start the threads
    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()
