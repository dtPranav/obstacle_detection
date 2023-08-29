import subprocess
import pyttsx3
import sys
import os
import time
import gc
from rich.traceback import install
from rich.table import Table
install()
table = Table(title='Obstacles')
table.add_column("Number",style='cyan')
table.add_column("Object",style='magenta')
table.add_column("Distance",style='green')
# ANSI escape sequences for text styles and colors
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
ITALIC = "\033[3m"
RESET = "\033[0m"
BLINK = "\033[5m"
import time

animation = ["|", "/", "-", "\\"]

# Text colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
try:
    print(f"{BOLD}{GREEN}[+] Core Started...{RESET}")

    def convert_to_speech(text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate * 4)
        engine.say(text)
        engine.runAndWait()

    python_executable = sys.executable

    command = ["python", "./detect.py", "--source", "0"]
    full_path = r"./detect.py"

    full_path = full_path.replace("\\\\", "\\")

    environment = os.environ.copy()
    environment["PATH"] = os.path.dirname(python_executable) + os.pathsep + environment["PATH"]

    print(f"{BOLD}{GREEN}[+] Clearing Output File...{RESET}")
    with open('./output.txt', "w") as file:
        file.truncate(0)

    
    print(f"{BOLD}{GREEN}[+] Detection Started...{RESET}")
    process = subprocess.Popen([python_executable, full_path, "--source", "0"], env=environment,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    flag=0
    content = process.stdout.readline()
    content = ""
    i=0
    print("\n")
    while i<100:
        print(f"{MAGENTA}\rLoading... {animation[i % len(animation)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\n")
    while True:
        content = process.stdout.readline()
        if 'dist:' in content:
            cont_list = content[3:].split('|')
            if len(cont_list[1].split(',')) <= 1:
                cont = str(cont_list[0]+' at '+cont_list[1].split(':')[1])
                print(f"{CYAN}{cont}")
                convert_to_speech(cont)
            else: 
                # cont = str(content)
                obs=cont_list[0].split(',')
                dis=cont_list[1].split(',')
                cont = ""
                for i in range(0,len(obs)-1):
                    cont += str(obs[i]+' at '+dis[i].split(':')[1] + '\t')
                print(f"{CYAN}{cont}")
                convert_to_speech(cont)

        # if not line:
        #     break
        # stdout_buffer.append(line.decode().strip())
        # with open('./output.txt', "r") as file:
        #     content = file.read().strip()
        #     if content:
        #         print(content)
        #         convert_to_speech(content)
        # # Clear the data that has been read from the file
        # with open('./output.txt', "w") as file:
        #     file.write(content[len(content):])
        # time.sleep(10)  # Delay between file checks
    # Wait for the YOLOv5 process to finish
    process.communicate()

except KeyboardInterrupt:
    print(f"{BOLD}{RED}[-] Keyboard Interrupt...{RESET}")
except Exception as e:
    print(f"{BOLD}{RED}[-] Exception Occured : {str(e)}{RESET}")
finally:
    if process:
        print(f"{BOLD}{RED}[-] Detection Termination Started...{RESET}")
        process.terminate()
        # Wait for the subprocess to exit
        process.wait(timeout=20)

        if process.poll() is None:
            process.kill()

        if process.returncode == 0 :
            print(f"{BOLD}{RED}[-] [-] Detection Terminated Successfully...{RESET}")
        else:
            print(f"{BOLD}{RED}[-] Detection Termination Timed Out so Killed...{RESET}")
        # If the subprocess did not exit, kill it forcefully

        process = None
    gc.collect()
    print(f"{BOLD}{RED}[-] Core Terminated...{RESET}")
    sys.exit()
