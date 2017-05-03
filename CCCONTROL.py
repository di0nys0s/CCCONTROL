#!/usr/bin/env python

import os
import curses
import configparser
import json
import subprocess
import re

def getnumcalcv2(adresse,user):
    process = subprocess.Popen(["ssh", user+"@"+adresse, " showq -u "+user], stdout=subprocess.PIPE)
    p = re.compile(b'(\d+) active jobs')
    while True:
        line = process.stdout.readline()
        if p.match(line):
            print('Numer of active process on colosse are '+str(p.findall(line)[0]))
            #ap.findall(line)[0])
        elif line != b'':
            os.write(1, line)
        else:
            break


def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def getnumcalc(adresse,user):
     os.system("clear")
     a = os.popen("ssh "+user+"@"+adresse+" showq -u "+user).read()
     for line in a.readline():
         print(line)
     input("Press Enter to continue...")
     print("")

def execute_cmd(cmd_string):
     os.system("clear")
     a = os.system(cmd_string)
     #a = system(cmd_string).read()
     print("")
     if a == 0:
          print("Command executed correctly")
     else:
          print("Command terminated with error")
     input("Press Enter to continue...")
     print("")

x = 0
config = configparser.ConfigParser()
config.read('/home/francois/.CQONTROL.cfg')
computers = json.loads(config.get('SYSTEM', 'computers'))
while x != ord('q'):
     screen = curses.initscr()

     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, "Please enter a number...")
     for i in range(len(computers)):
        screen.addstr(4+i, 4, str(i+1)+" - "+computers[i])

     #screen.addstr(4, 4, "1 - Add a user")
     #screen.addstr(5, 4, "2 - Restart Apache")
     #screen.addstr(6, 4, "3 - Show disk space")
     screen.addstr(len(computers)+6, 4, str(len(computers)+2)+" - Add a computer")
     screen.addstr(len(computers)+7, 4, "q - Exit")
     screen.refresh()

     x = screen.getch()
     for i in range(len(computers)):
        if x == ord(str(i+1)):
          adresse = config.get(computers[i],'adresse')
          user = config.get(computers[i],'user')
          curses.endwin()
          getnumcalcv2(adresse,user)
          #execute_cmd("ssh "+user+"@"+adresse+" showq -u "+user)
          #subprocess.check_output(['ssh', user+"@"+adresse, "showq -u "+user])
     #if x == ord('2'):
     #     curses.endwin()
     #     execute_cmd("apachectl restart")
     #if x == ord('3'):
     #     curses.endwin()
     #     execute_cmd("df -h")

curses.endwin()
