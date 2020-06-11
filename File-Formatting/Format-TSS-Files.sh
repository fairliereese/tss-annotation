cellType=$1
mode=$2
threshold=$3

dataDir=/data/tss_annotations
scriptDir=~/Scripts/tss-annotation/File-Formatting
ccres=$dataDir/Chromatin-Datasets/cCREs/hg38/$cellType/$cellType-cCREs.bed
rankedList=$dataDir/Transcription-Datasets/$mode/hg38/$cellType/$cellType-$mode-*Peak-Quantifications.txt
peakList=$dataDir/Transcription-Datasets/$mode/hg38/All-Biosamples-$mode-*Peaks.bed


if [ $mode == "RAMPAGE" ]
then
    col=3
    exp="RPM"
    peak="rPeaks"
elif [ $mode == "CAGE" ]
then
    col=2
    exp="TPM"
    peak="Peaks"
fi

awk '{if (NR != 1 && $'$col' >= '$threshold') print $0}' $rankedList | \
    sort -k1,1 > tmp.expression

awk 'FNR==NR {x[$1];next} ($4 in x)' tmp.expression $peakList > tmp.peaks

python $scriptDir/make-tss-bed.py tmp.expression tmp.peaks $mode > \
    $cellType-$mode-$peak.$exp-$threshold.bed

rm tmp.*
