# For Multi threading

import threading
import subprocess

def run_stealth_writer():
    print("\n*****Stealth Writer Process Running*****\n")
    subprocess.run(['python', 'stealthWriter.py'])
    # if result.returncode == 0:
    print("\n*****Stealth Writer Process is terminated*****\n")


def run_gpt_score():
    print("\n*****GptZero Process Running*****\n")
    subprocess.run(['python', 'gptScore.py'])
    # if result.returncode == 0:
    print("\n*****GptZero Process is terminated*****\n")

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
