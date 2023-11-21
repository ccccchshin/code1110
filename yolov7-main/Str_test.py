import os
import subprocess
import ServerTest

test = "no i "

def send(args):
    test = args
    return test


if __name__ == "__main__":
    result = subprocess.run(['python', 'ServerTest.py'], stdout=subprocess.PIPE, text=True)
    print(result.stdout)

