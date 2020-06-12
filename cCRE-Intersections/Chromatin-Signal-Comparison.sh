cellType=$1
dataDir=/data/tss_annotations/

ccreGroups=$cellType-PLS-Overlap-Groups.bed
ccreMaster=$dataDir/Chromatin-Datasets/cCREs/hg38/All-Biosamples-cCREs.bed 


awk 'FNR==NR {x[$4];next} ($5 in x)' $ccreGroups $ccreMaster | sort -k4,4 > tmp.ccre
sort -k4,4 $ccreGroups | awk 'BEGIN{print "cCRE" "\t" "Group"}\
    {print $4 "\t" $NF}' > tmp.matrix


signals=(DNase H3K4me3 H3K27ac CTCF)
for signal in ${signals[@]}
do
    echo $signal
    signalFile=$dataDir/Chromatin-Datasets/cCREs/hg38/$cellType/Signal-Files/$signal-Signal.txt 
    awk 'FNR==NR {x[$4];next} ($1 in x)' tmp.ccre $signalFile | sort -k1,1 > tmp.sig
    paste tmp.ccre tmp.sig | awk '{print $5 "\t" $9}' | sort -k1,1 | \
        awk 'BEGIN{print "'$signal'"}{print $2}' > tmp.col
    paste tmp.matrix tmp.col > tmp.out
    mv tmp.out tmp.matrix
done

mv tmp.matrix $cellType-PLS-Overlap-Signals.txt
rm tmp.*
