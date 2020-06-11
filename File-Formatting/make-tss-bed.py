import sys, math

def Create_Expression_Dict(expression):
    expressionDict={}
    maximum=0
    for line in expression:
        line=line.rstrip().split("\t")
        expressionDict[line[0]]=float(line[1])
        if float(line[1]) > maximum:
            maximum=float(line[1])
    maximum=math.log10(maximum)
    return expressionDict, maximum


expression=open(sys.argv[1])
expressionDict, maximum = Create_Expression_Dict(expression)
expression.close()

mode=sys.argv[3]

peaks=open(sys.argv[2])
for line in peaks:
    line=line.rstrip().split("\t")
    peakExp=expressionDict[line[3]]
    score=int(math.log10(peakExp)/maximum*1000)
    if mode == "RAMPAGE":
        print("\t".join(line[0:4])+"\t"+str(score)+"\t"+"\t".join(line[5:])+"\t"+str(round(peakExp,1)))
    elif mode == "CAGE":
        print("\t".join(line[0:4])+"\t"+str(score)+"\t"+line[5]+"\t"+line[1]+"\t"+line[2]+"\t"+ \
            line[8]+"\t"+line[7]+"\t"+str(round(peakExp,1)))
peaks.close()
