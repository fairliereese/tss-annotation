import sys


ccreDict={"PLS":0,"pELS":0,"dELS":0,"DNase-H3K4me3":0,"CTCF-only":0,"DNase-only":0}
ccreOrder=["PLS","pELS","dELS","DNase-H3K4me3","CTCF-only","DNase-only"]
total=0.0

inputData=open(sys.argv[1])

for line in inputData:
    line=line.rstrip().split("\t")
    line[9]=line[9].split(",")[0]
    if line[9] not in ccreDict:
        ccreDict[line[9]]=1
    else:
        ccreDict[line[9]]+=1
    total+=1

output=""
for group in ccreOrder:
    output+="\t"+str(ccreDict[group]/total*100)

print(output)


