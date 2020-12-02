while getopts a:d:c:o: flag
do
    case "${flag}" in
        a) annot_file=${OPTARG};;
        d) datasets=${OPTARG};;
        c) chrom_sizes=${OPTARG};;
		o) oprefix=${OPTARG};;
    esac
done

if [ -z "$datasets" ]
then
	datasets='all'
fi

# get single bp read ends from the talon read_annot file
python get_all_talon_annot_ends.py \
    -annot ${annot_file} \
    -datasets ${datasets} \
    -o ${oprefix}

# create a bigwig for TSSs and TESs; one file for each
# fwd and rev strands
bedGraphToBigWig \
	${oprefix}_fwd_tss.bedgraph \
	${chrom_sizes} \
	${oprefix}_fwd_tss.bw
bedGraphToBigWig \
	${oprefix}_rev_tss.bedgraph \
	${chrom_sizes} \
	${oprefix}_rev_tss.bw
bedGraphToBigWig \
	${oprefix}_fwd_tes.bedgraph \
	${chrom_sizes} \
	${oprefix}_fwd_tes.bw
bedGraphToBigWig \
	${oprefix}_rev_tes.bedgraph \
	${chrom_sizes} \
	${oprefix}_rev_tes.bw