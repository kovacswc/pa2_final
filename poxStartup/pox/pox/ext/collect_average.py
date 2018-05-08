from os import listdir
from os.path import isfile, join
import re
import os

#From mininet
def _parseIperf( iperfOutput ):
        """Parse iperf output and return bandwidth.
           iperfOutput: string
           returns: result string"""
        r = r'([\d\.]+ \w+/sec)'
        m = re.findall( r, iperfOutput )
        if m:
            return m[-1]
        else:
            # was: raise Exception(...)
            return ''


resultsPath = "~/results/clients/"

singleCount = 0
singleThroughput = 0
eightCount = 0
eightThroughput = 0
totalCount = 0
#Run through directory, parse iperf results, and get final output
for fn in listdir(os.path.expanduser(resultsPath)):
    fn_path = os.path.expanduser(resultsPath)+fn
    if fn.endswith("one.txt"):
        with open(fn_path, "r") as myfile:
            totalCount += 1
            data = myfile.readlines()
            sData = ""
            
            tpStr = _parseIperf(sData.join(data))
            if tpStr == '':
                continue

            singleCount += 1
            divM = 1
            if "Mbits" in tpStr:
                divM = 1000
            elif "Kbits" in tpStr:
                divM = 1000000
            tpStr = tpStr[:-10]
            singleThroughput += (float(tpStr)/divM)
            
    elif fn.endswith("eight.txt"):
        
        with open(fn_path, "r") as myfile:
            data = myfile.readlines()
            sData = ""
            tpStr = _parseIperf(sData.join(data))
            if tpStr == '':
                continue
            eightCount += 1
            divM = 1
            if "Mbits" in tpStr:
                    divM = 1000
            elif "Kbits" in tpStr:
                divM = 1000000

            tpStr = tpStr[:-10]
            eightThroughput += (float(tpStr)/divM)


singleAverage = 0
eightAverage = 0
if singleCount:
    singleAverage = singleThroughput/singleCount

if eightCount:
    eightAverage = eightThroughput/eightCount
print "Single flow throughput proportion: " + str(singleAverage)
print "Eight flow throughput proportion: " + str(eightAverage)
print "Number of pairs: " + str(totalCount)
print "Number of iperf restuls from single: " + str(singleCount)
print "Number of iperf results from eigh: " + str(eightCount)
