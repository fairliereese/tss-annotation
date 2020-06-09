library(ggplot2)
library(reshape)
library(gridExtra)

args <- commandArgs(trailingOnly = TRUE)
cellType=args[1]
mode=args[2]

tssIntersection=read.table(paste(mode,"-",cellType,"-TSS-Overlap.txt",sep=""))
ccreIntersection=read.table(paste(mode,"-",cellType,"-cCRE-Overlap.txt",sep=""))

rank=tssIntersection$V1[which.max(tssIntersection$V2 < 2)]

p1=ggplot(tssIntersection, aes(x=V1, y=V4))+geom_line()+geom_point()+
    xlab("Rank")+ylab("% overlap cCREs")+coord_cartesian(y=c(0,100))+
    geom_vline(xintercept=rank, color="red", linetype="dashed")
p2=ggplot(tssIntersection, aes(x=log10(V2), y=V4))+geom_line()+geom_point()+
    xlab("log10(TPM or RPM)")+ylab("% overlap cCREs")+coord_cartesian(y=c(0,100))+
    geom_vline(xintercept=log10(2), color="red", linetype="dashed")

png(paste(mode,"-",cellType,"-TSS-Overlap.png",sep=""), height=4, width=10, units="in", res=300)
grid.arrange(p1, p2, ncol=2)
dev.off()

ccreMelted=melt(ccreIntersection, id=c("V1","V2"))

p3=ggplot(ccreMelted, aes(x=V1, y=value, color=variable))+geom_line()+geom_point()+
    xlab("Rank")+ylab("% of overlapping cCREs")+coord_cartesian(y=c(0,100))+
    geom_vline(xintercept=rank, color="black", linetype="dashed")+
    scale_color_manual(values=c("#FF0000","#FFA700","#FFCD00","#ffaaaa","#00B0F0","#06DA93"))+
    theme(legend.position="none")

p4=ggplot(ccreMelted, aes(x=log10(V2), y=value, color=variable))+geom_line()+geom_point()+
    xlab("log10(TPM or RPM)")+ylab("% of overlapping cCREs")+coord_cartesian(y=c(0,100))+
    geom_vline(xintercept=log10(2), color="black", linetype="dashed")+
    scale_color_manual(values=c("#FF0000","#FFA700","#FFCD00","#ffaaaa","#00B0F0","#06DA93"))+
    theme(legend.position="none")

png(paste(mode,"-",cellType,"-cCRE-Overlap.png",sep=""), height=4, width=10, units="in", res=300)
grid.arrange(p3, p4, ncol=2)
dev.off()



