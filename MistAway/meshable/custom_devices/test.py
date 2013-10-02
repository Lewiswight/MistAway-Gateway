import os
import time
import sys

lastTime = 0
firstTime = True
time.sleep(300)
failCount = 0
while True:
    
    
    try:
        t = time.time()
        pid = os.popen("ps -ef | awk '/[d]pdsrv/{print $2}'")
        ppid = pid.readline()
        ppid = ppid.split("\n")
        print ppid
        runTime = os.popen("""ps aux | grep " """ + str(ppid[0]) + """ " | grep -v grep""") 
        print "here is the run time"
        runSec = runTime.readline()
        print runSec
        runSec = runSec.split(" ")
        print runSec
        for itm in runSec:
            if ":" in itm:
                realTime = itm
        print realTime
        realTime = realTime.replace(":", ".")
        print realTime
        print lastTime
        realTime = float(realTime)
        if firstTime == True:
            firstTime = False
            realTime = lastTime
            time.sleep(360)
            continue 
        with open("./log.txt", "a") as myfile:
                myfile.write("OLD CPU TIME: " + str(lastTime) + "  NEW CPU TIME: " + str(realTime) + chr(13))
        if realTime > lastTime:
            lastTime = realTime
            
        else:
            with open("./log.txt", "a") as myfile:
                myfile.write("reset at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + chr(13))
                os.system("reboot")
                myfile.close()
                break
        
        time.sleep(300)
    except:
        print "failed for the: " + str(failCount) + " time"
        failCount += 1
        if failCount > 15:
            with open("./log.txt", "a") as myfile:
                myfile.write("reset from errors at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + chr(13))
                os.system("reboot")
                myfile.close()
            os.system("reboot")
            break
        else:
            time.sleep(60)
            continue
        
    """
    t = time.time()
    hostname = "google.com" #example
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        with open("./log.txt", "a") as myfile:
            myfile.write(hostname +"  was up at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + chr(13))
            print hostname, 'is up! at:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
            myfile.close()
    else:
        time.sleep(60)
        response = os.system("ping -c 1 " + hostname)
        if response == 0:
            continue
        else:
            time.sleep(60)
            response = os.system("ping -c 1 " + hostname)
            if response == 0:
                continue
            else:
                time.sleep(60)
                response = os.system("ping -c 1 " + hostname)
                if response == 0:
                    continue 
                else:
                    print hostname, 'is down!'
                    with open("./log.txt", "a") as myfile:
                        myfile.write(hostname +"  reset at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + chr(13))
                        os.system("reboot")
                        myfile.close()
                        break
    
      
    time.sleep(120)"""
    
sys.exit(0)