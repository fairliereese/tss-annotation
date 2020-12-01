python get_ends_from_talon_annot.py \
	-annot sequel1/K562_TALON_gencodev29_v29_2019-05-24_talon_read_annot.tsv \
	-datasets D10,D11 \
	-filter_type talon \
	-min_tpm 1 \
	-o sequel1/PacBio_K562_Sequel1

python get_ends_from_talon_annot.py \
	-annot sequel2/GM12878_talon_read_annot.tsv \
	-datasets PB_GM12878_R1,PB_GM12878_R2 \
	-filter_type talon \
	-min_tpm 1 \
	-o sequel2/PacBio_GM12878_Sequel2

python get_ends_from_talon_annot.py \
	-annot sequel2/GM12878_talon_read_annot.tsv \
	-datasets ONT_GM12878_R1,ONT_GM12878_R2 \
	-filter_type talon \
	-min_tpm 1 \
	-o ont_dRNA/ONT_dRNA_GM12878

# TSS analysis

jamb_dir=/Users/fairliereese/mortazavi_lab/data/200609_jamboree/
ont_dir=${jamb_dir}ont_dRNA/
s2_dir=${jamb_dir}sequel2/
s1_dir=${jamb_dir}sequel1/

# read guys
read_ont_gm_tss=${ont_dir}ONT_dRNA_GM12878_TSS_sorted.bed
read_pb_gm_tss=${s2_dir}PacBio_GM12878_Sequel2_TSS_sorted.bed
read_pb_k5_tss=${s1_dir}PacBio_K562_Sequel1_TSS_sorted.bed

# read annots
annot_ont_gm_tss=${ont_dir}ONT_dRNA_GM12878_read_annot_TSS.tsv
annot_pb_gm_tss=${s2_dir}PacBio_GM12878_Sequel2_read_annot_TSS.tsv
annot_pb_k5_tss=${s1_dir}PacBio_K562_Sequel1_read_annot_TSS.tsv

# filtered guys
filt_ont_gm_tss=${ont_dir}ONT_dRNA_GM12878_TSS_1.0_tpm_filt.bed
filt_pb_gm_tss=${s2_dir}PacBio_GM12878_Sequel2_TSS_1.0_tpm_filt.bed
filt_pb_k5_tss=${s1_dir}PacBio_K562_Sequel1_TSS_1.0_tpm_filt.bed

# reference guys
gencode_tss=/Users/fairliereese/mortazavi_lab/ref/gencode.v29/gencode.v29.tss.bed

# first, we want to see how many merged ends we found were know or novel
python compare_ends_v_gencode.py \
	-bedfile $filt_ont_gm_tss \
	-ref $gencode_tss \
	-type TSS \
	-o gencode_v_ont_gm

python compare_ends_v_gencode.py \
	-bedfile $filt_pb_gm_tss \
	-ref $gencode_tss \
	-type TSS \
	-o gencode_v_pb_gm

python compare_ends_v_gencode.py \
	-bedfile $filt_pb_k5_tss \
	-ref $gencode_tss \
	-type TSS \
	-o gencode_v_pb_k5

# then, we want to see how our PacBio GM12878 data compares to the ONT GM12878 data
mkdir figures
python compare_ont_pb_ends.py \
	-bed_1 $filt_pb_gm_tss \
	-bed_1_type PacBio \
	-bed_2 $filt_ont_gm_tss \
	-bed_2_type ONT \
	-type TSS \
	-celltype GM12878 \
	-o ont_v_pb_gm12878

# how does each read map to the merged consensus ends?
python compare_ends_reads_v_consensus.py \
	-merged_ends $filt_pb_gm_tss \
	-read_ends $read_pb_gm_tss \
	-annot $annot_pb_gm_tss \
	-type TSS \
	-sample PB_GM12878 \
	-o ${s2_dir}pb_gm12878

python compare_ends_reads_v_consensus.py \
	-merged_ends $filt_ont_gm_tss \
	-read_ends $read_ont_gm_tss \
	-annot $annot_ont_gm_tss \
	-type TSS \
	-sample ONT_GM12878 \
	-o ${ont_dir}ont_gm12878

python compare_ends_reads_v_consensus.py \
	-merged_ends $filt_pb_k5_tss \
	-read_ends $read_pb_k5_tss \
	-annot $annot_pb_k5_tss \
	-type TSS \
	-sample PB_K562 \
	-o ${s1_dir}pb_k562


# TES analysis
# read guys
read_ont_gm_tes=${ont_dir}ONT_dRNA_GM12878_TES_sorted.bed
read_pb_gm_tes=${s2_dir}PacBio_GM12878_Sequel2_TES_sorted.bed
read_pb_k5_tes=${s1_dir}PacBio_K562_Sequel1_TES_sorted.bed

# read annots
annot_ont_gm_tes=${ont_dir}ONT_dRNA_GM12878_read_annot_TES.tsv
annot_pb_gm_tes=${s2_dir}PacBio_GM12878_Sequel2_read_annot_TES.tsv
annot_pb_k5_tes=${s1_dir}PacBio_K562_Sequel1_read_annot_TES.tsv

# filtered guys
filt_ont_gm_tes=${ont_dir}ONT_dRNA_GM12878_TES_1.0_tpm_filt.bed
filt_pb_gm_tes=${s2_dir}PacBio_GM12878_Sequel2_TES_1.0_tpm_filt.bed
filt_pb_k5_tes=${s1_dir}PacBio_K562_Sequel1_TES_1.0_tpm_filt.bed

# reference guys
gencode_tes=/Users/fairliereese/mortazavi_lab/ref/gencode.v29/gencode.v29.tes.bed

# first, we want to see how many merged ends we found were know or novel
python compare_ends_v_gencode.py \
	-bedfile $filt_ont_gm_tes \
	-ref $gencode_tes \
	-type TES \
	-o gencode_v_ont_gm

python compare_ends_v_gencode.py \
	-bedfile $filt_pb_gm_tes \
	-ref $gencode_tes \
	-type TES \
	-o gencode_v_pb_gm

python compare_ends_v_gencode.py \
	-bedfile $filt_pb_k5_tes \
	-ref $gencode_tes \
	-type TES \
	-o gencode_v_pb_k5

# then, we want to see how our PacBio GM12878 data compares to the ONT GM12878 data
mkdir figures
python compare_ont_pb_ends.py \
	-bed_1 $filt_pb_gm_tes \
	-bed_1_type PacBio \
	-bed_2 $filt_ont_gm_tes \
	-bed_2_type ONT \
	-type TES \
	-celltype GM12878 \
	-o ont_v_pb_gm12878_tes

# how does each read map to the merged consensus ends?
python compare_ends_reads_v_consensus.py \
	-merged_ends $filt_pb_gm_tes \
	-read_ends $read_pb_gm_tes \
	-annot $annot_pb_gm_tes \
	-type TES \
	-sample PB_GM12878 \
	-o ${s2_dir}pb_gm12878

python compare_ends_reads_v_consensus.py \
	-merged_ends $filt_ont_gm_tes \
	-read_ends $read_ont_gm_tes \
	-annot $annot_ont_gm_tes \
	-type TES \
	-sample ONT_GM12878 \
	-o ${ont_dir}ont_gm12878

python compare_ends_reads_v_consensus.py \
	-merged_ends $filt_pb_k5_tes \
	-read_ends $read_pb_k5_tes \
	-annot $annot_pb_k5_tes \
	-type TES \
	-sample PB_K562 \
	-o ${s1_dir}pb_k562


