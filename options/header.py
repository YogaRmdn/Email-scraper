from colors.color import *
import os
import platform

def clear_screen():
    os.system("cls" if platform == "nt" else "clear")


def header():
    print(f"""{BOLD_BLACK}
 ███▄ ▄███▓ ▄▄▄       ██▓ ██▓    
▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    
▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    
▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    
▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒
░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░
░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░
░      ░     ░   ▒    ▒ ░  ░ ░   
       ░         ░  ░ ░      ░  ░
      
      Author  : Yoga ramadani
    https://github.com/YogaRmdn
{RESET}""")