from time import gmtime, strftime

def WriteLog(msg):
    with open('log.txt', 'a') as logfile:
        logfile.write(strftime("%Y-%m-%d %H:%M:%S - ", gmtime())+msg+'\n')