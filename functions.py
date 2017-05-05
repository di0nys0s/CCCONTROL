import re
import subprocess
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
