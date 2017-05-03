#!/usr/bin/env python

import os
import curses
import configparser
import json
import subprocess
import re
import numpy as np
class calcul():
    def __init__(self):
        self.computer = ""
        self.id = ""
        self.state = ""
        self.walltime = ""
        self.rep = ""

def getnumcalcv2(adresse,user):
    process = subprocess.Popen(["ssh", user+"@"+adresse, " showq -u "+user], stdout=subprocess.PIPE)
    p = re.compile(b'(\d+) active job')
    p2 = re.compile(b'(\d+) eligible job')
    p3 = re.compile(b'(\d+) blocked job')
    p4 = re.compile(b'(\d+)\s+\w+\s+Running')

    i=0
    j=0
    k=0
    actjob=""
    while True:
        line = process.stdout.readline()
        if p.match(line):
            numactcalc=int(p.findall(line)[0])
            print('Numer of active process on colosse are '+str(numactcalc))
        elif p2.match(line):
            numelcalc=int(p2.findall(line)[0])
            print('Numer of eligible process on colosse are '+str(numelcalc))
        elif p3.match(line):
            numblockcalc=int(p3.findall(line)[0])
            print('Numer of blocked process on colosse are '+str(numblockcalc))
        elif p4.match(line):
            actjob=actjob+' '+str(p4.findall(line)[0])
        elif line == b'':
            break
    return numactcalc,numelcalc,numblockcalc,actjob


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
def updatenumcalc():
    screen.addstr(len(computers)+10, 4, "---- "+computers[0]+" ----")
    screen.addstr(len(computers)+11, 4, "- Running Calculation = "+str(numactcalc[0]))
    screen.addstr(len(computers)+12, 4, "- Elligible Calculation = "+str(numelcalc[0]))
    screen.addstr(len(computers)+13, 4, "- Blocked Calculation = "+str(numblockcalc[0]))

    screen.addstr(len(computers)+10, 4+35, "---- "+computers[1]+" ----")
    screen.addstr(len(computers)+11, 4+35, "- Running Calculation = "+str(numactcalc[1]))
    screen.addstr(len(computers)+12, 4+35, "- Elligible Calculation = "+str(numelcalc[1]))
    screen.addstr(len(computers)+13, 4+35, "- Blocked Calculation = "+str(numblockcalc[1]))

    screen.addstr(len(computers)+10, 4+70, "---- "+computers[2]+" ----")
    screen.addstr(len(computers)+11, 4+70, "- Running Calculation = "+str(numactcalc[2]))
    screen.addstr(len(computers)+12, 4+70, "- Elligible Calculation = "+str(numelcalc[2]))
    screen.addstr(len(computers)+13, 4+70, "- Blocked Calculation = "+str(numblockcalc[2]))
def getactid(adresse,user,processstdout,numactcalc):
    print('PROCESS=')
    print(str(processstdout))
    p = re.compile(b'(\d+) ^\w+$ Running')
    p2 = re.compile(b'(\d+) eligible job')
    actcalc=np.zeros(numactcalc, dtype=np.int)
    i=0
    while True:
        line = processstdout.readline()
        print(str(line))
        if p.match(line):
            actcalc[i]=int(p.findall(line)[0])
            i=i+1
            print('process '+str(i)+' = '+str(actcalc[i]))
        elif p2.match(line):
            numelcalc=int(p2.findall(line)[0])
            print('IN GETACTID Numer of eligible process on colosse are '+str(numelcalc))
        elif line == b'':
            break    
    return actcalc


config = configparser.ConfigParser()
config.read('/home/francois/.CCCONTROL/CCCONTROL.cfg')
computers = json.loads(config.get('SYSTEM', 'computers'))
numactcalc=np.zeros(len(computers), dtype=np.int)
numelcalc=np.zeros(len(computers), dtype=np.int)
numblockcalc=np.zeros(len(computers), dtype=np.int)
screen = curses.initscr()
def main():
    screen.clear()
    screen.border(0)
    updatenumcalc()

    x = 0
    while x != ord('q'):
     screen.addstr(2, 2, "Please enter a number...")
     for i in range(len(computers)):
        screen.addstr(4+i, 4, str(i+1)+" - "+computers[i])

     screen.addstr(len(computers)+6, 4, str(len(computers)+2)+" - Add a computer")
     screen.addstr(len(computers)+7, 4, "q - Exit")
     screen.refresh()

     x = screen.getch()
     for i in range(len(computers)):
        if x == ord(str(i+1)):
          adresse = config.get(computers[i],'adresse')
          user = config.get(computers[i],'user')
          curses.endwin()
          numactcalc[i],numelcalc[i],numblockcalc[i],actjob=getnumcalcv2(adresse,user)
          print('active job')
          print(actjob)
          #actcalc=np.zeros(numactcalc[i], dtype=np.int)
          #elcalc=np.zeros(numelcalc[i], dtype=np.int)
          #blockcalc=np.zeros(numblockcalc[i], dtype=np.int)
          #actcalc=getactid(adresse,user,processstdout,numactcalc[i])

          screen.clear()
          screen.border(0)
          screen.addstr(4,2,"------------ "+computers[i]+" ------------")
          screen.addstr(len(computers)+11, 4, "- Running Calculation = "+str(numactcalc[i]))
          screen.addstr(len(computers)+12, 4, "- Elligible Calculation = "+str(numelcalc[i]))
          screen.addstr(len(computers)+13, 4, "- Blocked Calculation = "+str(numblockcalc[i]))
          x = screen.getch()
          if x == ord('b'):
              main()
main()
curses.endwin()

